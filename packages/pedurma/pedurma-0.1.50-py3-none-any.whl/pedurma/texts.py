import json
import re
from collections import defaultdict
from pathlib import Path

import requests
from openpecha.serializers import HFMLSerializer
from openpecha.utils import download_pecha, load_yaml

from pedurma import config
from pedurma.exceptions import TextMappingNotFound
from pedurma.pecha import NotesPage, Page, PedurmaText, Text
from pedurma.utils import get_pages


def get_text_info(text_id, index):
    texts = index["annotations"]
    for uuid, text in texts.items():
        if text["work_id"] == text_id:
            return (uuid, text)
    return ("", "")


def get_meta_data(pecha_id, text_uuid, meta_data):
    meta = {}
    source_meta = meta_data.get("source_metadata", "")
    if source_meta:
        meta = {
            "work_id": source_meta.get("work_id", ""),
            "img_grp_offset": source_meta.get("img_grp_offset", ""),
            "pref": source_meta.get("pref", ""),
            "pecha_id": pecha_id,
            "text_uuid": text_uuid,
        }
    return meta


def get_hfml_text(opf_path, text_id, index=None):
    serializer = HFMLSerializer(
        opf_path, text_id=text_id, index_layer=index, layers=["Pagination", "Durchen"]
    )
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text


def get_body_text(text_with_durchen):
    body_text = ""
    pages = get_pages(text_with_durchen)
    for page in pages:
        if re.search("<[𰵀-󴉱]?d", page):
            return body_text
        body_text += page
    return body_text


def get_durchen(text_with_durchen):
    durchen = ""
    durchen_start = False
    pages = get_pages(text_with_durchen)
    for page in pages:
        if re.search("<[𰵀-󴉱]?d", page) or durchen_start:
            durchen += page
            durchen_start = True
        if re.search("d>", page):
            return durchen
    if not durchen:
        print("INFO: durchen not found..")
    return durchen


def get_page_id(img_num, pagination_layer):
    paginations = pagination_layer["annotations"]
    for uuid, pagination in paginations.items():
        if pagination["imgnum"] == img_num:
            return uuid
    return ""


def get_link(img_num, vol_meta):
    image_grp_id = vol_meta["image_group_id"]
    link = f"https://iiif.bdrc.io/bdr:{image_grp_id}::{image_grp_id}{int(img_num):04}.jpg/full/max/0/default.jpg"
    return link


def get_note_ref(img_num, pagination_layer):
    paginations = pagination_layer["annotations"]
    for uuid, pagination in paginations.items():
        if pagination["imgnum"] == img_num:
            try:
                return pagination["note_ref"]
            except Exception:
                return ""
    return ""


def get_note_refs(img_num, pagination_layer):
    note_refs = []
    cur_pg_note_ref = get_note_ref(img_num, pagination_layer)
    note_refs.append(cur_pg_note_ref)
    next_pg_note_ref = get_note_ref(img_num + 1, pagination_layer)
    if next_pg_note_ref and cur_pg_note_ref != next_pg_note_ref:
        note_refs.append(next_pg_note_ref)
    return note_refs


def get_clean_page(page):
    pat_list = {
        "page_pattern": r"〔[𰵀-󴉱]?\d+〕",
        "topic_pattern": r"\{([𰵀-󴉱])?\w+\}",
        "start_durchen_pattern": r"\<([𰵀-󴉱])?d",
        "end_durchen_pattern": r"d\>",
        "sub_topic_pattern": r"\{([𰵀-󴉱])?\w+\-\w+\}",
    }
    base_page = page
    for ann, ann_pat in pat_list.items():
        base_page = re.sub(ann_pat, "", base_page)
    base_page = base_page.strip()
    return base_page


def get_page_obj(page, vol_meta, tag, pagination_layer):
    img_num = int(re.search(r"〔[𰵀-󴉱]?(\d+)〕", page).group(1))
    page_id = get_page_id(img_num, pagination_layer)
    page_content = get_clean_page(page)
    page_link = get_link(img_num, vol_meta)
    note_ref = get_note_refs(img_num, pagination_layer)
    if page_content == "":
        page_obj = None
    else:
        if tag == "note":
            page_obj = NotesPage(
                id=page_id,
                page_no=img_num,
                content=page_content,
                name=f"Page {img_num}",
                vol=vol_meta["volume_number"],
                image_link=page_link,
            )
        else:
            page_obj = Page(
                id=page_id,
                page_no=img_num,
                content=page_content,
                name=f"Page {img_num}",
                vol=vol_meta["volume_number"],
                image_link=page_link,
                note_ref=note_ref,
            )

    return page_obj


def get_page_obj_list(text, vol_meta, pagination_layer, tag="text"):
    page_obj_list = []
    pages = get_pages(text)
    for page in pages:
        pg_obj = get_page_obj(page, vol_meta, tag, pagination_layer)
        if pg_obj:
            page_obj_list.append(pg_obj)
    return page_obj_list


def get_vol_meta(vol_num, pecha_meta):
    vol_meta = {}
    vol_num = int(vol_num[1:])
    text_vols = pecha_meta["source_metadata"].get("volumes", {})
    if text_vols:
        for vol_id, vol in text_vols.items():
            if vol["volume_number"] == vol_num:
                vol_meta = vol
    return vol_meta


def get_first_note_pg(notes, vol_meta):
    for note in notes:
        if int(note.vol) == vol_meta["volume_number"]:
            return note
    return None


def get_cur_vol_notes(notes, vol_meta):
    cur_vol_notes = []
    for note in notes:
        if int(note.vol) == vol_meta["volume_number"]:
            cur_vol_notes.append(note)
    return cur_vol_notes


def get_last_page_note_ref(notes, vol_meta):
    cur_vol_notes = get_cur_vol_notes(notes, vol_meta)
    last_page_note_refs = []
    if len(cur_vol_notes) >= 2:
        last_page_note_refs = [cur_vol_notes[-2].id, cur_vol_notes[-1].id, "--"]
    elif len(cur_vol_notes) == 1:
        last_page_note_refs = [cur_vol_notes[-1].id, "--"]
    else:
        last_page_note_refs = ["--"]
    return last_page_note_refs


def get_last_pg_content(first_note_pg):
    last_pg_content = first_note_pg.content
    pg_ann = ""
    if re.search(r"<p(\d+-\d+)>", last_pg_content):
        pg_ann = re.search(r"<p(\d+-\d+)>", last_pg_content).group(1)
    if re.search("བསྡུར་མཆན", last_pg_content):
        new_pg_end = re.search("བསྡུར་མཆན", last_pg_content).end()
        last_pg_content = f"{last_pg_content[:new_pg_end]}\n{pg_ann}\n"
    else:
        last_pg_content = re.sub(r"<p(\d+-\d+)>", pg_ann, last_pg_content)
    return last_pg_content


def get_last_page(pages, notes, vol_meta):
    if pages[-1].note_ref[0] != notes[-1].id:
        pages[-1].note_ref.insert(1, notes[-1].id)
    first_note_pg = get_first_note_pg(notes, vol_meta)
    pg_content = get_last_pg_content(first_note_pg)
    note_refs = get_last_page_note_ref(notes, vol_meta)
    last_page = Page(
        id=first_note_pg.id,
        page_no=first_note_pg.page_no,
        content=pg_content,
        name=f"Page {first_note_pg.page_no}",
        vol=first_note_pg.vol,
        image_link=first_note_pg.image_link,
        note_ref=note_refs,
    )
    pages.append(last_page)
    return pages


def construct_text_obj(hfmls, pecha_meta, opf_path):
    pages = []
    notes = []
    for vol_num, hfml_text in hfmls.items():
        vol_meta = get_vol_meta(vol_num, pecha_meta)
        pagination_layer = load_yaml(
            Path(f"{opf_path}/{pecha_meta['id']}.opf/layers/{vol_num}/Pagination.yml")
        )
        durchen = get_durchen(hfml_text)
        body_text = get_body_text(hfml_text)

        pages += get_page_obj_list(body_text, vol_meta, pagination_layer, tag="text")
        if durchen:
            notes += get_page_obj_list(durchen, vol_meta, pagination_layer, tag="note")
        if notes:
            pages = get_last_page(pages, notes, vol_meta)
    text_obj = Text(id=pecha_meta["text_uuid"], pages=pages, notes=notes)
    return text_obj


def get_last_pg_ann(page):
    pg_ann = ""
    page_content = page.content
    vol = page.vol
    if re.search(fr"{vol}-\d+", page_content):
        pg_ann = re.search(fr"{vol}-\d+", page_content)[0]
    return pg_ann


def get_body_text_from_last_page(page):
    body_part = ""
    last_page = page.content
    if re.search("བསྡུར་མཆན", last_page):
        durchen_start_pat = re.search("བསྡུར་མཆན", last_page)
        body_part = last_page[: durchen_start_pat.start()]
    return body_part


def get_note_text_from_first_note_page(note):
    first_page = note.content
    note_part = first_page
    if re.search("བསྡུར་མཆན", first_page):
        durchen_start_pat = re.search("བསྡུར་མཆན", first_page)
        note_part = first_page[durchen_start_pat.start() :]
    return note_part


def get_first_note_content(page, note):
    first_note_content = ""
    body_part = get_body_text_from_last_page(page)
    note_part = get_note_text_from_first_note_page(note)
    first_note_content = body_part + note_part
    return first_note_content


def merge_last_pg_with_note_pg(text, page):
    first_note = None
    for pg_walker, note in enumerate(text.notes):
        if note.vol == page.vol:
            first_note = note
            break
    text.notes[pg_walker].content = get_first_note_content(page, first_note)


def remove_last_pages(text):
    new_pages = []
    for pg_walker, page in enumerate(text.pages):
        if "--" in page.note_ref:
            merge_last_pg_with_note_pg(text, page)
            continue
        new_pages.append(page)
    new_text = Text(id=text.id, pages=new_pages, notes=text.notes)
    return new_text


def serialize_text_obj(text):
    """Serialize text object to hfml

    Args:
        text (obj): text object

    Returns:
        dict: vol as key and value as hfml
    """
    text_hfml = defaultdict(str)
    pages = text.pages
    notes = text.notes
    for page in pages:
        text_hfml[f"v{int(page.vol):03}"] += f"{page.content}\n\n"
    for note in notes:
        text_hfml[f"v{int(note.vol):03}"] += f"{note.content}\n\n"
    return text_hfml


def get_durchen_page_objs(page, notes):
    note_objs = []
    for note in notes:
        if note.id in page.note_ref:
            note_objs.append(note)
    return note_objs


def get_pecha_paths(text_id, text_mapping=None):
    pecha_paths = {"namsel": None, "google": None}
    if not text_mapping:
        text_mapping = requests.get(config.TEXT_LIST_URL)
        text_mapping = json.loads(text_mapping.text)
    text_info = text_mapping.get(text_id, {})
    if text_info:
        pecha_paths["namsel"] = download_pecha(text_info["namsel"])
        pecha_paths["google"] = download_pecha(text_info["google"])
    else:
        raise TextMappingNotFound
    return pecha_paths


def get_text_obj(pecha_id, text_id, pecha_path=None):
    if not pecha_path:
        pecha_path = download_pecha(pecha_id, needs_update=False)
    pecha_meta = load_yaml(Path(f"{pecha_path}/{pecha_id}.opf/meta.yml"))
    index = load_yaml(Path(f"{pecha_path}/{pecha_id}.opf/index.yml"))
    hfmls = get_hfml_text(f"{pecha_path}/{pecha_id}.opf/", text_id, index)
    text_uuid, text = get_text_info(text_id, index)
    pecha_meta["text_uuid"] = text_uuid
    text = construct_text_obj(hfmls, pecha_meta, pecha_path)
    return text


def get_pedurma_text_obj(text_id, pecha_paths=None):
    if not pecha_paths:
        pecha_paths = get_pecha_paths(text_id)
    text = {}
    for pecha_src, pecha_path in pecha_paths.items():
        pecha_id = Path(pecha_path).stem
        text[pecha_src] = get_text_obj(pecha_id, text_id, pecha_path)
    pedurma_text = PedurmaText(
        text_id=text_id, namsel=text["namsel"], google=text["google"]
    )
    return pedurma_text

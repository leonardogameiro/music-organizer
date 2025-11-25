import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Music Organizer", layout="wide")
st.title("🎵 Music Playlist Organizer")

ROOT = Path(__file__).resolve().parent
CSV  = ROOT / "data" / "songs_sample.csv"  # expects data/songs_sample.csv next to this file

try:
    df = pd.read_csv(CSV)
except Exception as e:
    st.error(f"Couldn't load CSV at: {CSV}")
    st.exception(e)
    st.stop()

# normalize minimal columns so it won't crash if some are missing
for c in ["title","artist","album","genre","mood","year","duration_sec"]:
    if c not in df.columns:
        df[c] = "" if c not in ("year","duration_sec") else 0

df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
df["duration_sec"] = pd.to_numeric(df["duration_sec"], errors="coerce").fillna(0).astype(int)

st.success(f"Loaded {len(df)} songs")

col1, col2, col3 = st.columns([2,2,3])
with col1:
    g = st.selectbox("Genre", ["(any)"] + sorted([x for x in df["genre"].dropna().unique() if x]))
with col2:
    m = st.selectbox("Mood",  ["(any)"] + sorted([x for x in df["mood"].dropna().unique() if x]))
with col3:
    q = st.text_input("Search title/artist/album")

view = df.copy()
if g != "(any)": view = view[view["genre"].str.lower()==g.lower()]
if m != "(any)": view = view[view["mood"].str.lower()==m.lower()]
if q:
    qq = q.lower()
    view = view[view[["title","artist","album"]].apply(lambda r: any(qq in str(v).lower() for v in r), axis=1)]

st.write(f"Showing {len(view)} songs")
st.dataframe(view, use_container_width=True, hide_index=True)


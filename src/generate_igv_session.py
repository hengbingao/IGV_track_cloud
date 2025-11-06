#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Automatically generate an IGV session XML file
- Input file: one bigWig per line
  Supports:
    1) One-column (just URL)
    2) Two-column (track_name and URL, separated by tab or space)
- Track name = first column if provided, else filename from URL
"""

import argparse
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    """Recursively indent XML for pretty printing"""
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for e in elem:
            indent(e, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def generate_igv_session(input_file, output_file, genome="hg38"):
    # Root session element
    session = ET.Element("Session", {
        "genome": genome,
        "hasGeneTrack": "true",
        "hasSequenceTrack": "true",
        "locus": "All",
        "version": "8"
    })

    # Resources & Panels
    resources = ET.SubElement(session, "Resources")

    data_panel = ET.SubElement(session, "Panel", {
        "height": "534",
        "name": "DataPanel",
        "width": "1778"
    })

    feature_panel = ET.SubElement(session, "Panel", {
        "height": "302",
        "name": "FeaturePanel",
        "width": "1778"
    })

    # Reference sequence and gene tracks
    ET.SubElement(feature_panel, "Track", {
        "clazz": "org.broad.igv.track.SequenceTrack",
        "fontSize": "10",
        "id": "Reference sequence",
        "name": "Reference sequence",
        "visible": "true"
    })

    if genome.lower() == "hg38":
        gene_id = "hg38_genes"
        gene_name = "Gene"
        color_scale_max = "845.0"
    elif genome.lower() == "mm10":
        gene_id = "mm10_genes"
        gene_name = "Refseq genes"
        color_scale_max = "406.0"
    else:
        gene_id = f"{genome}_genes"
        gene_name = "Gene"
        color_scale_max = "845.0"

    ET.SubElement(feature_panel, "Track", {
        "clazz": "org.broad.igv.track.FeatureTrack",
        "color": "0,0,178",
        "colorScale": f"ContinuousColorScale;0.0;{color_scale_max};255,255,255;0,0,178",
        "fontSize": "10",
        "height": "35",
        "id": gene_id,
        "name": gene_name,
        "visible": "true"
    })

    # --- Read input file ---
    track_entries = []
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 1:
                track_name = parts[0].split("/")[-1].split("?")[0]
                url = parts[0]
            else:
                track_name, url = parts[0], parts[1]

            # Ensure Dropbox direct download
            if "dropbox.com" in url:
                url = url.replace("?dl=0", "?dl=1").replace("&dl=0", "&dl=1")

            track_entries.append((track_name, url))

    # --- Add each track ---
    for track_name, url in track_entries:
        ET.SubElement(resources, "Resource", {"path": url})

        track = ET.SubElement(data_panel, "Track", {
            "autoScale": "false",
            "clazz": "org.broad.igv.track.DataSourceTrack",
            "fontSize": "10",
            "id": url,
            "name": track_name,
            "renderer": "BAR_CHART",
            "visible": "true",
            "windowFunction": "mean"
        })
        ET.SubElement(track, "DataRange", {
            "baseline": "0.0",
            "drawBaseline": "true",
            "flipAxis": "false",
            "maximum": "1.0",
            "minimum": "0.0",
            "type": "LINEAR"
        })

    # --- Layout & hidden attributes ---
    ET.SubElement(session, "PanelLayout", {"dividerFractions": "0.6358244365361803"})
    hidden = ET.SubElement(session, "HiddenAttributes")
    ET.SubElement(hidden, "Attribute", {"name": "DATA FILE"})
    ET.SubElement(hidden, "Attribute", {"name": "DATA TYPE"})
    ET.SubElement(hidden, "Attribute", {"name": "NAME"})

    indent(session)
    tree = ET.ElementTree(session)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    print(f"? IGV session saved to {output_file}")
    print(f"Included {len(track_entries)} tracks.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate IGV session XML file")
    parser.add_argument("-i", "--input", required=True, help="Input file: either one URL per line or two columns (track_name URL)")
    parser.add_argument("-o", "--output", default="igv_session.xml", help="Output XML file name")
    parser.add_argument("-g", "--genome", default="hg38", help="Genome assembly (e.g. hg38, mm10)")
    args = parser.parse_args()

    generate_igv_session(args.input, args.output, genome=args.genome)

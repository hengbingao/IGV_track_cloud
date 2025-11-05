#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Automatically generate an IGV session XML file
- Input file: one bigWig URL per line
- Track name = bigWig filename
- Supports multiple genomes (hg38, mm10, etc.)
- Outputs a pretty-printed XML similar to IGV export
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
        "locus": "All",  # default locus, could also allow user input
        "version": "8"
    })

    # Resources
    resources = ET.SubElement(session, "Resources")

    # DataPanel
    data_panel = ET.SubElement(session, "Panel", {
        "height": "534",
        "name": "DataPanel",
        "width": "1778"
    })

    # FeaturePanel
    feature_panel = ET.SubElement(session, "Panel", {
        "height": "302",
        "name": "FeaturePanel",
        "width": "1778"
    })

    # Reference and gene tracks
    ET.SubElement(feature_panel, "Track", {
        "clazz": "org.broad.igv.track.SequenceTrack",
        "fontSize": "10",
        "id": "Reference sequence",
        "name": "Reference sequence",
        "visible": "true"
    })

    # Gene track differs depending on genome
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
        color_scale_max = "845.0"  # default

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

    # Read URLs
    with open(input_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        # Convert Dropbox links to dl=1
        if "dropbox.com" in url:
            if "?dl=0" in url:
                url = url.replace("?dl=0", "?dl=1")
            elif "&dl=0" in url:
                url = url.replace("&dl=0", "&dl=1")

        # Add to Resources
        ET.SubElement(resources, "Resource", {"path": url})

        # Track name = bigWig filename
        track_name = url.split("/")[-1].split("?")[0]

        # Add track to DataPanel
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

    # PanelLayout and HiddenAttributes
    ET.SubElement(session, "PanelLayout", {"dividerFractions": "0.6358244365361803"})
    hidden = ET.SubElement(session, "HiddenAttributes")
    ET.SubElement(hidden, "Attribute", {"name": "DATA FILE"})
    ET.SubElement(hidden, "Attribute", {"name": "DATA TYPE"})
    ET.SubElement(hidden, "Attribute", {"name": "NAME"})

    # Pretty print
    indent(session)

    # Save XML
    tree = ET.ElementTree(session)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    print(f"IGV session saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate IGV session XML file")
    parser.add_argument("-i", "--input", required=True, help="Input file, one bigWig URL per line")
    parser.add_argument("-o", "--output", default="igv_session.xml", help="Output session XML file")
    parser.add_argument("-g", "--genome", default="hg38", help="Reference genome (e.g., hg38, mm10)")
    args = parser.parse_args()

    generate_igv_session(args.input, args.output, genome=args.genome)

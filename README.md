# IGV_cloud_tracks

Generate IGV session XML files from cloud-hosted bigWig files with support for multiple genomes (hg38, mm10)

![IGV session example](https://github.com/hengbingao/IGV_track_cloud/blob/main/png/IGV_cloud_tracks.png)

## **Install**

1. Clone the repository:

    ```bash
    git clone https://github.com/hengbingao/IGV_track_cloud.git
    ```

2. Set executable permissions:

    ```bash
    cd IGV_track_cloud
    chmod +x ./bin/*
    chmod +x ./src/*
    ```

3. Add to environment:

    ```bash
    echo "export PATH=$PATH:$(pwd)/bin" >> ~/.bashrc
    source ~/.bashrc
    ```

4. Install Python dependencies (required for Dropbox functionality):

    ```bash
    pip install dropbox
    ```

## **Usage**

1. Show help:

    ```bash
    IGV_cloud_tracks --help/-h
    ```

2. **Quick Parameter Reference Table**

| Subcommand            | Parameter                  | Shortcut | Description                                                                 |
|-----------------------|---------------------------|---------|-----------------------------------------------------------------------------|
| `-dropbox_URL`         | `--key`                    | `-k`    | Dropbox API access token (required)                                         |
|                       | `--folder`                 | `-f`    | Dropbox folder path (required)                                              |
|                       | `--output`                 | `-o`    | Output file for URLs (default: `dropbox_links.txt`)                          |
| `-igv_session_xml`      | `--input`                  | `-i`    | Input file with URLs or two-column `track_name URL`                          |
|                       | `--output`                 | `-o`    | Output IGV session XML file (default: `igv_session.xml`)                     |
|                       | `--genome`                 | `-g`    | Reference genome (`hg38` or `mm10`, default: `hg38`)                         |

**Important notes for Dropbox usage:**

- You must have a Dropbox API access token. Generate one at: [Dropbox Developers Apps](https://www.dropbox.com/developers/apps/info/b2d7u4n267ude1y)  
- Ensure your app permission is set to **sharing.write** , the you can get the from **Generated access token** which under **setting**
- The output file will contain **two columns**: `filename <TAB> direct_download_URL`  

3. **Generate Dropbox URLs (`-dropbox_URL`)**

    ```bash
    IGV_cloud_tracks -dropbox_URL -k <ACCESS_TOKEN> -f <DROPBOX_FOLDER> [-o <OUTPUT_FILE>]
    ```

   **Example:**

    ```bash
    IGV_cloud_tracks -dropbox_URL -k sl.ABCDEF123456 -f /CUTnTag/hs/ -o hs_links.txt
    ```

4. **Generate an IGV session XML file (`-igv_session_xml`)**

    ```bash
    IGV_cloud_tracks -igv_session_xml -i <INPUT_FILE> [-o <OUTPUT_FILE>] [-g <GENOME>]
    ```

    **Example 1: Using Dropbox-generated links**

    ```bash
    IGV_cloud_tracks -igv_session_xml -i hs_links.txt -o hs_session.xml -g hg38
    ```

    **Example 2: Using custom track names**

    ```bash
    IGV_cloud_tracks -igv_session_xml -i my_tracks.txt -o my_session.xml -g mm10
    ```

**Notes:**

- Track names in the IGV session are automatically taken from the first column of the input file (if provided) or from the bigWig filename  
- Dropbox links are converted to direct download links (`?dl=1`)  
- Supports multiple genomes via the `-g` option  

5. **Full workflow example**

    ```bash
    # Step 1: Generate Dropbox URLs for a folder
    IGV_cloud_tracks -dropbox_URL -k <ACCESS_TOKEN> -f /CUTnTag/hs/ -o hs_links.txt

    # Step 2: Generate an IGV session XML using these URLs
    IGV_cloud_tracks -igv_session_xml -i hs_links.txt -o hs_session.xml -g hg38
    ```

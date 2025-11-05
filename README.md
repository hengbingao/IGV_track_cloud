# IGV_cloud_tracks
Generate IGV session XML files from cloud-hosted bigWig files with support for multiple genomes (hg38, mm10)

![IGV session example](https://github.com/hengbingao/IGV_track_cloud/blob/main/png/IGV_cloud_tracks.png)

## **Install**

1. Clone the repository:

    ```bash
    git clone https://github.com/hengbingao/IGV_cloud_tracks.git
    ```

2. Set executable permissions:

    ```bash
    cd IGV_cloud_tracks
    chmod +x ./bin/*
    chmod +x ./src/*
    ```

3. Add to environment:

    ```bash
    echo "export PATH=\$PATH:$(pwd)/bin" >> ~/.bashrc
    source ~/.bashrc
    ```

## **Usage**

1. Show help:

    ```bash
    IGV_cloud_tracks --help/-h
    ```

2. Generate an IGV session XML file:

    ```bash
    IGV_cloud_tracks -i cloud_tracks.txt -o my_session.xml -g hg38
    ```

- `-i, --input` : Input file with cloud-hosted bigWig URLs (one per line)  
- `-o, --output`: Output IGV session XML file (default: `igv_session.xml`)  
- `-g, --genome`: Reference genome (`hg38` or `mm10`, default: `hg38`)  

3. Example:

    ```bash
    IGV_cloud_tracks -i cloud_tracks.txt
    ```

    ```bash
    IGV_cloud_tracks -i mm10_tracks.txt -o mm10_session.xml -g mm10
    ```

- Track names in the IGV session are automatically taken from the bigWig filenames  
- Dropbox links are converted to direct download links (`?dl=1`)  
- Supports multiple genomes via the `-g` option

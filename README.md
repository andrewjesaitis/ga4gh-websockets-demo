# ga4gh-websockets-demo
Just a little demo using websockets as a streaming implementation

## Get it

```
git clone git@github.com:andrewjesaitis/ga4gh-websockets-demo.git
cd ga4gh-websockets-demo
pip install -r requirements.txt
```

## Back it

```
cd ga4gh-websockets-demo/data/release
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi
```

## Run it

```
python server.py
<open another terminal>
python client.py
```

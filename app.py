import urllib3
import click
import certifi

@click.group()
def cli():
    pass

@cli.command()
def download():
    """This subcommand gets the dataset from an url, unzips it and organizes 
    the files by storing 80% of them in the train folder and the remaining
    20% in the test folder"""
#    downloadURL = "http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip"
    downloadURL = "https://drive.google.com/uc?authuser=0&id=1vIBUOOUGC1z_Uhr-"
    + "f3XhOo0drY-YYf63&export=download"
    myFile = "Test.rar"
    http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
    r = http.request('GET', downloadURL, timeout=4.0)
    output = open(myFile,'wb')
    output.write(r.data)
    output.close()

if __name__ == "__main__":
    cli()

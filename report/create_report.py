# write a script to create a folder

import os

def create_report():
    os.makedirs('report', exist_ok=True)

    # tlhv
    os.chdir('report')
    os.makedirs('extract', exist_ok=True)
    os.chdir('extract')
    os.system('cp ../../../extract_features_from_data/extract_data.py .')

    # lqt
    os.chdir('..')
    os.makedirs('crawl_data', exist_ok=True)
    os.chdir('crawl_data')
    os.system('cp ../../../crawl-data-and-get-coordinates/parallel_crawling.py .')

    # lpt
    os.chdir('..')
    os.system("cp -r ../../EDA_FE/ .")
    os.chdir("EDA_FE")
    os.system("rm README.md")
    os.system("rm Scaler.ipynb")
    os.system("rm foliumClusterVisualization.html")
    os.chdir('..')
    os.rename("EDA_FE", "eda")

    # dxt
    os.makedirs('train', exist_ok=True)
    os.chdir('train')
    os.system('cp ../../../train/train.ipynb .')
    os.system("cp ../../../train_complex/pytorch.ipynb .")
    os.system("cp ../../../train_complex/random_forest.ipynb .")

    # data
    os.chdir('..')
    os.system('cp -r ../../data/ .')

if __name__ == '__main__':
    create_report()

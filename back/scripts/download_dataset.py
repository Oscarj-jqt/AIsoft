from icrawler.builtin import BingImageCrawler
import os

classes = {
    "ak47": "ak47 gun",
    "glock": "glock pistol",
    "beretta": "beretta gun",
    "revolver": "revolver handgun"
}

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dataset"))

os.makedirs(output_dir, exist_ok=True)

for class_name, query in classes.items():
    class_dir = os.path.join(output_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)

    print(f"Téléchargement de : {query}")
    BingImageCrawler(storage={"root_dir": class_dir}).crawl(
        keyword=query,
        max_num=200
    )

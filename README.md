# GoldenAnpu-SubClassAnnotation
Provides annotation support for the GoldenAnpu sweet pepper dataset to convert it to the University of Bonn BUP variants.


# Create the virtual environment

Using python3 create your virtual environment

You may need to follow [this](https://askubuntu.com/questions/1434956/install-qt6-on-22-04) guide to install PyQt6 on your machine.

```python3 -m venv venv-GUI```


```>>> . venv-GUI/bin/activate```
```>>> pip3 install -r requirements.txt```


# Download the GoldenAnpu Sweet Pepper Dataset

Go to [here](https://github.com/dataset-ninja/sweet-pepper) and then click on the ```DOWNLOAD.md``` document and follow the prompts.

You'll find the meta file for their dataset [here](files/meta.json) that you need to put in the root directory you downloaded.

# Run the annotation tool

```>>> python main.py --root <root location of the dataset> --imageloc <direct location to the images> --annoloc <direct location to the image jsons> --output <where you'd like to save the corrosponding smap and imap images>```

# How to use the annotation tool

![Screenshot of the Application](images/GUI.png)

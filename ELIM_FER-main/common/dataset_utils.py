import os
import pandas as pd
import numpy as np

from PIL import Image

from torch.utils.data import Dataset
from fabulous.color import fg256


class FaceDataset(Dataset):

    def __init__(self, csv_file, root_dir, transform=None, inFolder=None, landmarks=False):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.training_sheet = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        if inFolder is None:
            self.inFolder = np.full((len(self.training_sheet),), True)
        
        self.loc_list = np.where(inFolder)[0]
        self.infold = self.inFolder
        
    def __len__(self):
        return  np.sum(self.infold*1)

    def __getitem__(self, idx):

        img_name = os.path.join(self.root_dir, self.training_sheet.iloc[idx, 0])
        valence = self.training_sheet.iloc[idx,1] * 1.0
        arousal = self.training_sheet.iloc[idx,2] * 1.0
        
        sample = Image.open(img_name)
        
        if self.transform:
            sample = self.transform(sample)
        return {'image': sample, 'va': [valence, arousal], 'path': self.training_sheet.iloc[idx, 0]}


class FaceDataset_AffectNet(Dataset):

    def __init__(self, csv_file, root_dir, transform=None, inFolder=None, landmarks=False):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.training_sheet = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        if inFolder is None:
            self.inFolder = np.full((len(self.training_sheet),), True)
        
        self.loc_list = np.where(inFolder)[0]
        self.infold = self.inFolder
        
    def __len__(self):
        return  np.sum(self.infold*1)

    def __getitem__(self, idx):

        img_name = os.path.join(self.root_dir, self.training_sheet.iloc[idx, 0])
        valence = self.training_sheet.iloc[idx,1]
        arousal = self.training_sheet.iloc[idx,2]
        age     = self.training_sheet.iloc[idx,9]
        
        sample = Image.open(img_name)
        
        if self.transform:
            sample = self.transform(sample)
        return {'image': sample, 'va': [valence, arousal], 'age': age}


class FaceDataset_Category(Dataset):

    def __init__(self, csv_file, root_dir, transform=None, inFolder=None, landmarks=False):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.training_sheet = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        if inFolder is None:
            self.inFolder = np.full((len(self.training_sheet),), True)
        
        self.loc_list = np.where(inFolder)[0]
        self.infold = self.inFolder
        
    def __len__(self):
        return  np.sum(self.infold*1)

    def __getitem__(self, idx):

        img_name   = os.path.join(self.root_dir, self.training_sheet.iloc[idx, 0])
        sample = Image.open(img_name)

        expression = self.training_sheet.iloc[idx,6]
        age        = self.training_sheet.iloc[idx,9]
        
        if self.transform:
            sample = self.transform(sample)
        return {'image': sample, 'exp': expression, 'age': age}

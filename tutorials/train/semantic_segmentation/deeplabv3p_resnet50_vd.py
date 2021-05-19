import paddlex as pdx
from paddlex import transforms

optic_dataset = 'https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz'
pdx.utils.download_and_decompress(optic_dataset, path='./')

train_transforms = transforms.Compose([
    transforms.Resize(target_size=512),
    transforms.RandomHorizontalFlip(),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

eval_transforms = transforms.Compose([
    transforms.Resize(target_size=512),
    transforms.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

train_dataset = pdx.datasets.SegDataset(
    data_dir='optic_disc_seg',
    file_list='optic_disc_seg/train_list.txt',
    label_list='optic_disc_seg/labels.txt',
    transforms=train_transforms,
    shuffle=True)

eval_dataset = pdx.datasets.SegDataset(
    data_dir='optic_disc_seg',
    file_list='optic_disc_seg/val_list.txt',
    label_list='optic_disc_seg/labels.txt',
    transforms=eval_transforms,
    shuffle=False)

num_classes = len(train_dataset.labels)
model = pdx.models.DeepLabV3P(num_classes=num_classes, backbone='ResNet50_vd')

model.train(
    num_epochs=10,
    train_dataset=train_dataset,
    train_batch_size=4,
    eval_dataset=eval_dataset,
    learning_rate=0.01,
    save_dir='output/deeplabv3p_r50vd')
import os
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision import transforms
from gan_module import Generator

# Argument parser
parser = ArgumentParser()
parser.add_argument('--image_path', type=str, help='The path to the image file')  # Ensure this line is present

@torch.no_grad()
def main():
    args = parser.parse_args()

    # Debugging: Print the parsed arguments
    print(f"Parsed arguments: {args}")

    # Check if the image path is valid
    if not os.path.isfile(args.image_path):
        print(f"Invalid file path: {args.image_path}")
        return

    #Load the pre-trained model
    model = Generator(ngf=32, n_residual_blocks=9)
    ckpt = torch.load('pretrained_model/state_dict.pth', map_location='cpu', weights_only=True)
    model.load_state_dict(ckpt)
    model.eval()

    # Transform the input image
    trans = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])
    
    # Load and process the input image
    img = Image.open(args.image_path).convert('RGB')
    img_tensor = trans(img).unsqueeze(0)

    # Apply the aging model
    aged_face = model(img_tensor)
    aged_face = (aged_face.squeeze().permute(1, 2, 0).numpy() + 1.0) / 2.0

    # Plot and save the original and aged images
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow((img_tensor.squeeze().permute(1, 2, 0).numpy() + 1.0) / 2.0)
    ax[0].set_title("Original Image")
    ax[1].imshow(aged_face)
    ax[1].set_title("Aged Image")
    
    plt.savefig("aged_output.png")  # Save the aged image


if __name__ == '__main__':
    main()

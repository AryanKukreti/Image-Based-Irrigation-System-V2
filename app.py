import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from utils.gui_utils import get_image_path
from utils.graph_utils import generate_graph
from utils.plot_utils import plot_results

def main():
    st.title("Irrigation Graph with Minimum Spanning Tree")

    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "bmp", "tiff"])

    if uploaded_file is not None:
        # Load the image and convert to grayscale
        image = Image.open(uploaded_file).convert("L")
        image_array = np.array(image)
        
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        st.write("Select the starting point for irrigation.")

        # Create a plot to display the image
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(image_array, cmap="gray", alpha=0.6)
        ax.set_title("Click to select the starting point")
        st.pyplot(fig)
        
        # Get the starting point from user input
        starting_point_x = st.slider("Select Starting Point X", 0, image_array.shape[1] - 1, value=image_array.shape[1] // 2)
        starting_point_y = st.slider("Select Starting Point Y", 0, image_array.shape[0] - 1, value=image_array.shape[0] // 2)
        starting_point = [starting_point_x, starting_point_y]

        # Check if the starting point is in a dark area (ditch)
        ditch_threshold = 60
        if image_array[starting_point_y, starting_point_x] < ditch_threshold:
            st.error("Sorry, but you can't plant the irrigation system here as it's over a ditch.")
            st.stop()  # Stop execution if the starting point is invalid

        # Generate random points avoiding dark areas
        num_points = 200
        points = []
        while len(points) < num_points:
            x = np.random.randint(0, image_array.shape[1])
            y = np.random.randint(0, image_array.shape[0])
            if image_array[y, x] > ditch_threshold:
                points.append([x, y])
        points = np.array(points)
        
        # Add the selected starting point to the points list
        points = np.vstack([starting_point, points])

        st.write("Generating graph and computing Minimum Spanning Tree...")
        
        # Perform Delaunay triangulation and generate the graph
        tri, G = generate_graph(points, image_array, ditch_threshold)
        
        # Compute the Minimum Spanning Tree and plot results
        mst = plot_results(tri, G, image_array, starting_point, points)

        # Save the plot as a PNG image to display in Streamlit
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        st.image(buffer, caption="Minimum Spanning Tree")

if __name__ == "__main__":
    main()

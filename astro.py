from astroquery.mast import Observations
import requests
import os

def download_jwst_photos(output_dir="jwst_photos"):
    """
    Downloads all JWST photos in their best available resolution.

    Args:
        output_dir (str): Directory to save the downloaded images.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Querying JWST observations...")
    # Query JWST observations
    jwst_observations = Observations.query_criteria(
        obs_collection="JWST",
        dataRights="PUBLIC"
    )
    
    # Filter for products (e.g., images)
    print("Getting product list...")
    products = Observations.get_product_list(jwst_observations)

    # Filter to download only science-grade image files
    best_quality = Observations.filter_products(
        products,
        productType="SCIENCE",
        extension="fits"  # JWST data typically uses FITS files
    )

    print(f"Found {len(best_quality)} files to download.")
    
    # Download files
    manifest = Observations.download_products(
        best_quality,
        download_dir=output_dir,
        mrp_only=True  # Download the most representative products
    )

    print(f"Download complete. Files saved to: {output_dir}")

if __name__ == "__main__":
    # Run the downloader
    download_jwst_photos()

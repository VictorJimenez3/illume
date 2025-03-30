from llm_engineering.infrastructure import get_mochi_output

# Get the volume
mochi_volume = get_mochi_output()

# Example: Read a specific file from the volume
file_contents = b"".join(mochi_volume.read_file("temp.mp4"))

print(file_contents)
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Rectangle, Polygon
import numpy as np
import io
import base64

def draw_promoter(ax, x, y, name):
    ax.plot([x, x], [y, y+0.5], 'k-', linewidth=2)
    ax.arrow(x, y+0.5, 0.1, 0, head_width=0.1, head_length=0.1, fc='k', ec='k',linewidth=2)
    ax.text(x+0.1, y+0.6, name, ha='center', va='bottom', rotation=45)
    return 0.2  # Width of promoter

def draw_gene(ax, x, y, width, name, color):
    ax.add_patch(Rectangle((x, y-0.25), width, 0.5, color=color))
    ax.arrow(x, y, width, 0, head_width=0.7, head_length=0.2, fc=color, ec=color)
    ax.text(x + width/2, y, name, ha='center', va='center')
    return width

def draw_terminator(ax, x, y, name):
    ax.plot([x, x], [y, y+0.5], 'k-', linewidth=2)
    ax.plot([x-0.1, x+0.1], [y+0.5, y+0.5], 'k-', linewidth=2)
    ax.text(x, y+0.6, name, ha='center', va='bottom', rotation=45)
    return 0.2  # Width of terminator

def create_plasmid_construct(plasmid_name, construct_string):
    parts = construct_string.split(',')
    
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_ylim(-1, 2)
    ax.axis('off')
    
    x = 1
    colors = plt.cm.Set3(np.linspace(0, 1, len(parts)))
    
    # Calculate the total width of all parts
    total_width = 0
    for part in parts:
        promoter, gene, terminator = part.split('-')
        total_width += 0.2  # promoter width
        total_width += 0.7  # gene width
        total_width += 0.2  # terminator width
        total_width += 0.3  # space between parts
    
    # Set the x-axis limit based on the total width
    ax.set_xlim(0.25, total_width + 2)  # Add padding on both sides
    
    # Calculate start and end points for the horizontal line
    line_start = 1-0.25  # Start of the first promoter
    line_end = total_width + 1  # End of the last terminator
    
    # Draw horizontal line
    ax.plot([line_start, line_end], [0, 0], 'k-', linewidth=2, zorder=0)
    
    for i, part in enumerate(parts):
        promoter, gene, terminator = part.split('-')
        
        x += draw_promoter(ax, x, 0, promoter)
        x += draw_gene(ax, x, 0, 0.7, gene, colors[i])
        x += draw_terminator(ax, x+0.3, 0, terminator)
        if i < len(parts):
            x += 0.3  # Space between parts, but not after the last part
    
    ax.set_title(f"Gene Circuit: {plasmid_name}")
    
    return fig

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.savefig(buffered, format="png", dpi=300)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.title('Genetic Circuit Visualizer')
    
    st.write("""
    This app visualizes genetic circuits. Enter the construct names and construct strings below.
    
    Format for each construct: circuit_name: promoter-gene-terminator,promoter-gene-terminator,...
    
    Example:
    pSynBio5000: pTEF1-GFP-tCYC1,pGAL1-RFP-tADH1
    pSynBio3000: pHXT7-RFP-tADH1,pTEF1-GFP-tCYC1
    """)
    
    constructs_input = st.text_area('Enter Constructs (one per line)', 
                                    'pSynBio5000: pTEF1-GFP-tCYC1,pGAL1-RFP-tADH1\npSynBio3000: pHXT7-RFP-tADH1,pTEF1-GFP-tCYC1')
    
    if st.button('Generate Visualizations'):
        constructs = constructs_input.strip().split('\n')
        if constructs:
            for construct in constructs:
                plasmid_name, construct_string = construct.split(':')
                plasmid_name = plasmid_name.strip()
                construct_string = construct_string.strip()
                
                fig = create_plasmid_construct(plasmid_name, construct_string)
                st.pyplot(fig)
                
                # Provide download link
                st.markdown(get_image_download_link(fig, f"{plasmid_name}.png", f'Download {plasmid_name} construct'), unsafe_allow_html=True)
                
                st.write('---')  # Separator between constructs
        else:
            st.warning('Please enter at least one construct.')

if __name__ == '__main__':
    main()
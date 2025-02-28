import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide' )

#Custom Css
st.markdown(
    """
<style>
.stApp{
background-color: black;
color: white;
}
</style>
""",
unsafe_allow_html=True
)

#title and description
st.title("✨📀Datasweeper Sterling Integrator By Rimsha Tariq")
st.write("Transform Your Files Between CSV And EXCEL formats with built-in data cleaning App")

#file uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or EXCEL):", type=["CSV", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)  

    else:
        st.error(f"unsupported file type: {file_ext}")
        "continue"

    #file details
    st.write("🔍 preview the head of the Dataframe")     
    st.dataframe(df.head())  

    #data cleaning option
    st.subheader("🚮Data Cleaning Options")
    if st.checkbox(f"Clean data for {file.name}"):
        col1, col2 = st.columns(2)

    with col1:   
        if st.button(f"✅Remove Duplicates from the File : {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("✅Duplicates Removed!")

    with col2:
        if st.button(f"✅Fill missing values for {file.name}"): 
            numeric_cols = df.select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("✅Missing values have been filled!")      

        st.subheader("📝Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
                
                
        #Data Visualization
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

       #Conversation Options

    st.subheader("🤝🏻Conversation Options")
    conversation_type = st.radio(f"Convert {file.name} to:", ["cvs" , "Excel"], key=file.name)
    if st.button(f"Convert{file.name}"):
        buffer = BytesIO()
        if conversation_type == "cvs":
           df.to.csv(buffer, index=False)
           file.name = file.name.replace (file_ext, ".csv")
           mime_type = "text/csv"

        elif conversation_type == "Excel":
           df.to_Excel(buffer, index=False)
        file.name = file.name.replace (file_ext, ".xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        st.download_button(
        label=f"Download {file.name} as {"conversion_type"}",
        data=buffer,
        file_name="file_name",
        mime=mime_type
        )
        st.success("🎉 All files processed successfully!")

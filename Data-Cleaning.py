import streamlit as st 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import io 

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Data Cleaning App",
    page_icon="🛠️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ===== BUTTON ===== */

    .stButton > button {
        background-color: #D6E6F7;
        color: #0A2540;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #DDE6ED;
        color: #1E3A8A;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ===== BUTTON ===== */

    .stButton > button {
        ...
    }


    /* ===== IQR INFORMATION ===== */

    .iqr-container {
        border: 1px solid #D1D5DB;
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .iqr-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .iqr-grid {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        flex-wrap: wrap;
    }

    .iqr-item {
        flex: 1;
        min-width: 120px;
        text-align: center;
    }

    .iqr-label {
        font-size: 14px;
        color: #6B7280;
    }

    .iqr-value {
        font-size: 22px;
        font-weight: bold;
        color: #1E293B;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "original_data" not in st.session_state:
    st.session_state.original_data = None

if "cleaned_data" not in st.session_state:
    st.session_state.cleaned_data = None

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

# Check whether data has been uploaded
is_data_active = st.session_state.cleaned_data is not None


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "<h2 style='margin-bottom:-10px;'>🛠️ Data Cleaning App</h2>",
    unsafe_allow_html=True
)
st.sidebar.info(
    "**Welcome!**\n\n"
    "Upload your dataset and use the tools below to clean, transform, and prepare your data.")

st.sidebar.write("")

# =========================
# DASHBOARD
# =========================

if st.sidebar.button(
    "📊 Dashboard",
    use_container_width=True,
    type="primary"
    if st.session_state.active_page == "Dashboard"
    else "secondary"
):
    st.session_state.active_page = "Dashboard"

# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------

st.sidebar.markdown("**📂 DATA**")

if st.sidebar.button(
    "Preview",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Preview"
    else "secondary"
):
    st.session_state.active_page = "Preview"


if st.sidebar.button(
    "Overview",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Overview"
    else "secondary"
):
    st.session_state.active_page = "Overview"


if st.sidebar.button(
    "Complete Summary",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Summary"
    else "secondary"
):
    st.session_state.active_page = "Summary"


# ------------------------------------------------------------
# DATA TRANSFORMATION  
# ------------------------------------------------------------

st.sidebar.markdown("**⚙️ TRANSFORMATION**")

if st.sidebar.button(
    "Data Transformation",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Transformation"
    else "secondary"
):
    st.session_state.active_page = "Transformation"


# ------------------------------------------------------------
# DATA CLEANING 
# ------------------------------------------------------------

st.sidebar.markdown("**🛠️ CLEANING**")

if st.sidebar.button(
    "Missing Values",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Missing"
    else "secondary"
):
    st.session_state.active_page = "Missing"


if st.sidebar.button(
    "Duplicates",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Duplicates"
    else "secondary"
):
    st.session_state.active_page = "Duplicates"


if st.sidebar.button(
    "Outliers",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Outliers"
    else "secondary"
):
    st.session_state.active_page = "Outliers"


# ------------------------------------------------------------
# OTHER 
# ------------------------------------------------------------

st.sidebar.markdown("**📋 OTHER**")

if st.sidebar.button(
    "Cleaning Log",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Cleaning log"
    else "secondary"
):
    st.session_state.active_page = "Cleaning Log"


if st.sidebar.button(
    "Download",
    use_container_width=True,
    disabled=not is_data_active,
    type="primary"
    if st.session_state.active_page == "Download"
    else "secondary"
):
    st.session_state.active_page = "Download"


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if st.session_state.active_page == "Dashboard":

    # --------------------------------------------------------
    # NO DATA
    # --------------------------------------------------------     

    if not is_data_active:

        st.markdown(
            "<h1 style='text-align: center;'>📊 Dashboard</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align: center; color: gray;'>"
            "Get a quick overview of your dataset and its current data quality."
            "</p>",
            unsafe_allow_html=True
        )

        st.write("")

        with st.container(border=True):

            uploaded_file = st.file_uploader(
                "📁 Upload A **CSV** or An **Excel** File And Clean Your Dataset Easily.",
                type=["csv", "xlsx", "xls"])

            if uploaded_file is not None:

                try:
                    # Get file extension
                    file_extension = (uploaded_file.name.split(".")[-1].lower())

                    # Read file based on extension
                    if file_extension == "csv":
                        data = pd.read_csv(uploaded_file)

                    elif file_extension in ["xlsx", "xls"]:
                        data = pd.read_excel(uploaded_file)

                    else:
                        st.error("Unsupported File Format.")
                        st.stop()


                    # Convert boolean columns to string
                    bool_cols = data.select_dtypes(include=["bool"]).columns
                    data[bool_cols] = data[bool_cols].astype("str")

                    # Check if a new file is uploaded 
                    if (
                        "file_name" not in st.session_state 
                        or st.session_state.file_name != uploaded_file.name):

                        # Save original dataset (never changes)
                        st.session_state.original_data = data.copy()

                        # Working dataset 
                        st.session_state.cleaned_data = data.copy()

                        # Cleaning history
                        st.session_state.history = []

                        # Save file name 
                        st.session_state.file_name = uploaded_file.name

                    st.success("✅ File uploaded successfully!")

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Could not read the CSV / Excel file. "
                        "Please check the file format."
                    )

                    st.exception(e)

            # --------------------------------------------------------
            # DATA LOADED
            # --------------------------------------------------------

    else:

        data = st.session_state.cleaned_data

        st.markdown(
            "<h1 style='text-align: center;'>📊 Dashboard</h1>",
            unsafe_allow_html=True)

        st.markdown(
            "<p style='text-align: center; color: gray;'>"
            "Get a quick overview of your dataset and its key information."
            "</p>",
            unsafe_allow_html=True)

        st.write("")

        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>"
            f"Dataset: 📄 {st.session_state.file_name}"
            f"</p>",
            unsafe_allow_html=True)

        st.write("")


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        with col_m1:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "🗂️ Rows"
                    "</p>",
                    unsafe_allow_html=True)

                st.markdown(f"## **{data.shape[0]:,}**")

        with col_m2:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "📋 Columns"
                    "</p>",
                    unsafe_allow_html=True)

                st.markdown(f"## **{data.shape[1]:,}**")

        with col_m3:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "❗ Missing"
                    "</p>",
                    unsafe_allow_html=True)

                total_missing = data.isna().sum().sum()

                st.markdown(f"## **{total_missing:,}**")


        with col_m4:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "🗄️ Duplicates"
                    "</p>",
                    unsafe_allow_html=True)

                total_dups = data.duplicated().sum()
                
                st.markdown(f"## **{total_dups:,}**")

        st.write("---")

        # ----------------------------------------------------
        # DATASET OVERVIEW
        # ----------------------------------------------------

        st.markdown(
                    '<h3 style="text-align: center; margin-top: 20px; margin-bottom: 25px;">'
                    'Dataset Overview'
                    '</h3>',
                    unsafe_allow_html=True
                    )

        # Calculate Values
        num_cols_count = len(data.select_dtypes(include=[np.number]).columns)
        cat_cols_count = len(data.select_dtypes(include=["object","category"]).columns)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                "<p style='text-align: center; color: gray;'>"
                "Numerical Columns"
                "</p>",
                unsafe_allow_html=True
                )

            st.markdown(
                f"<h2 style='text-align: center;'>{num_cols_count}</h2>",
                unsafe_allow_html=True
                )
            

        with col_right:
            st.markdown(
                "<p style='text-align: center; color: gray;'>"
                "Categorical Columns"
                "</p>",
                unsafe_allow_html=True
                )

            st.markdown(
                f"<h2 style='text-align: center;'>{cat_cols_count}</h2>",
                unsafe_allow_html=True
                )

        st.divider()

        # ----------------------------------------------------
        # DATASET INSIGHTS
        # ----------------------------------------------------   

        st.markdown(
            '<h3 style="text-align: center; margin-top: 20px; margin-bottom: 25px;">'
            'Dataset Insights'
            '</h3>',
            unsafe_allow_html=True
            )

        # Total number of cells 
        total_values = data.shape[0] * data.shape[1]

        # Total missing values
        total_missing = data.isna().sum().sum()

        # Missing value rate
        missing_rate = (
            (total_missing / total_values) * 100
            if total_values > 0
            else 0
            )

        # Memory usage
        memory_usage = data.memory_usage(deep=True).sum() / 1024

        # Mising values for each column 
        missing_by_column = data.isna().sum()

        # Most missing values
        missing_counts = data.isnull().sum()

        if missing_counts.max() == 0:
            most_missing = "None"
            most_missing_count = 0
        else:
            most_missing = missing_counts.idxmax()
            most_missing_count = missing_counts.max() 

        # ----------------------------------------------------
        # INSIGHT METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            with st.container(border=True):
                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "📊 Total Values"
                    "</p>",
                    unsafe_allow_html=True
                    )
                
                st.markdown(f"## **{total_values:,}**")

        with col2:
            with st.container(border=True):
                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "⚠️ Missing Rate"
                    "</p>",
                    unsafe_allow_html=True
                    )
       
                st.markdown(f"## **{missing_rate:.1f}%**")
            

        with col3:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "💾 Memory Usage"
                    "</p>",
                    unsafe_allow_html=True
                    )

                st.markdown(f"## **{memory_usage:.1f} KB**")

        with col4:

            with st.container(border=True):

                st.markdown(
                    "<p style='color: gray; font-size: 14px;'>"
                    "❗ Most Missing"
                    "</p>",
                    unsafe_allow_html=True
                    )

                if most_missing == "None":
                    st.markdown("## **None**")

                else:
                    st.markdown(f"## **{most_missing}**")

        st.divider()      

        # ----------------------------------------------------
        # RESET DATASET
        # ----------------------------------------------------      

        st.write("")      

        if st.button(
            "🔄 Reset / Upload Different Dataset",
            type="secondary",
            use_container_width=True
        ):

                st.session_state.original_data = None
                st.session_state.cleaned_data = None
                st.session_state.file_name = ""
                st.session_state.history = []

                st.session_state.active_page = "Dashboard"

                st.rerun()

# ============================================================
# PAGE 2 — PREVIEW
# ============================================================

elif st.session_state.active_page == "Preview":

    # Current working dataset
    data = st.session_state.cleaned_data

    st.markdown(
       "<h1 style='text-align: center;'>🗃️ Dataset Preview</h1>",
        unsafe_allow_html=True)

    st.markdown(
       "<p style='text-align: center; color: gray;'>"
        "Preview and compare your original and current dataset."
        "</p>",
        unsafe_allow_html=True)

    st.write("")

    # --------------------------------------------------------
    # RESET DATASET
    # --------------------------------------------------------

    reset_disabled = data.equals(st.session_state.original_data)

    if st.button(
        "🔄 Reset Dataset",
        disabled=reset_disabled
    ):

        st.session_state.cleaned_data = (
            st.session_state.original_data.copy()
        )

        st.session_state.history = []

        st.success("Dataset has been reset.")

        st.rerun()

    st.write("")

    # --------------------------------------------------------
    # DATASET TABS
    # --------------------------------------------------------

    tab1, tab2 = st.tabs(
        ["Original Dataset", "Current Dataset"]
    )

    # --------------------------------------------------------
    # ORIGINAL DATASET
    # --------------------------------------------------------

    with tab1:

        original = st.session_state.original_data

        rows_to_show = min(20, len(original))

        st.caption(
            f"Showing first {rows_to_show} of {len(original):,} rows"
        )

        st.dataframe(
            original.head(rows_to_show),
            use_container_width=True
        )

        st.write(
            f"**Shape:** {original.shape[0]:,} rows × "
            f"{original.shape[1]:,} columns"
        )

    # --------------------------------------------------------
    # CURRENT DATASET
    # --------------------------------------------------------

    with tab2:

        rows_to_show = min(20, len(data))

        st.caption(
        f"Showing first {rows_to_show} of {len(data):,} rows"
        )

        st.dataframe(
            data.head(rows_to_show),
            use_container_width=True
        )

        st.write(
            f"**Shape:** {data.shape[0]:,} rows × "
            f"{data.shape[1]:,} columns"
        )

# ============================================================
# PAGE 3 — OVERVIEW
# ============================================================

elif st.session_state.active_page == "Overview":

    # Current working dataset
    data = st.session_state.cleaned_data

    # --------------------------------------------------------
    # PAGE TITLE
    # --------------------------------------------------------
    
    st.markdown(
        "<h1 style='text-align: center;'>🔎 Dataset Overview</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "View your dataset structure, including column names, "
        "data types, and non-null values."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    st.markdown("### 📋 Column Information")
    st.caption("Review each column's data type and the number of non-null values.")

    dtypes_df = pd.DataFrame({
        "Column Name": data.columns,
        "Data Type": [str(t) for t in data.dtypes],
        "Non-Null Count": data.notna().sum().values
    })

    st.dataframe(
        dtypes_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PAGE 4 — COMPLETE SUMMARY
# ============================================================

elif st.session_state.active_page == "Summary":

    data = st.session_state.cleaned_data

    # --------------------------------------------------------
    # PAGE TITLE
    # --------------------------------------------------------

    st.markdown(
        "<h1 style='text-align: center;'>📝 Complete Summary</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "View detailed information about your dataset, including "
        "its structure, data types, and memory usage."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    st.markdown("### 📊 Dataset Information")
    st.caption("A complete summary of your dataset.")

    buffer = io.StringIO()

    data.info(buf=buffer)

    information = buffer.getvalue()

    st.code(information)


# ============================================================
# PAGE 5 — Transformation
# ============================================================

elif st.session_state.active_page == "Transformation":

    data = st.session_state.cleaned_data

    # --------------------------------------------------------
    # PAGE TITLE
    # --------------------------------------------------------

    st.markdown(
        "<h1 style='text-align: center;'>⚙️ Data Transformation</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Modify your dataset structure and column properties."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # ========================================================
    # DATA TYPES
    # ========================================================

    st.markdown("### 🔄 Data Types")

    st.caption(
        "View and change the data type of your dataset columns."
    )

    dtype_df = pd.DataFrame({
        "Column": data.columns,
        "Data Type": data.dtypes.astype(str).values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )

    # DEBUG
    # st.write("DEBUG: ", data.dtypes)

    st.write("")

    st.markdown("**Change Data Type**")

    column = st.selectbox(
        "Select Column",
        data.columns,
        key="dtype_column"
    )

    new_type = st.selectbox(
        "Convert To",
        ["Integer", "Float", "String", "Category", "Boolean"],
        key="new_type"
    )

    type_mapping = {
        "Integer": "Int64",
        "Float": "float64",
        "String": "string",
        "Category": "category",
        "Boolean": "bool"
    }

    if st.button(
        "🔄 Convert Data Type",
        use_container_width=True
    ):

        try:

            # ==================================================
            # NUMERIC CONVERSION
            # ==================================================

            if new_type in ["Integer", "Float"]:

                converted = pd.to_numeric(
                    data[column],
                    errors="coerce"
                )

                invalid_values = (
                    data[column].notna() & 
                    converted.isna()
                ).sum()

                # ----------------------------------------------
                # Integer
                # ----------------------------------------------

                if new_type == "Integer":

                    # check whether decimal values exist
                    decimal_values = (
                        converted.notna() & 
                        (converted % 1 != 0)
                    ).sum()

                    if decimal_values > 0:

                        st.error(
                            f"Cannot convert '{column}' to Integer "
                            f"because it contains {decimal_values} "
                            "decimal value(s)."
                        )

                        st.stop()

                    data[column] = converted.astype("Int64")

                # ----------------------------------------------
                # Float
                # ----------------------------------------------

                else:

                    data[column] = converted.astype("float64")


                # ----------------------------------------------
                # Invalid values
                # ----------------------------------------------

                if invalid_values > 0:

                    st.warning(
                        f"{invalid_values} invalid value(s) in "
                        f"'{column}' were converted to missing values."
                    )

                    st.session_state.history.append(
                       f"Converted '{column}' to {new_type}. "
                       f"{invalid_values} invalid value(s) became missing." 
                    )

                else:

                    st.session_state.history.append(
                       f"Converted '{column}' to {new_type}." 
                    )

            # ==================================================
            # OTHER DATA TYPES
            # ==================================================
            
            else:

                data[column] = data[column].astype(
                    type_mapping[new_type]
                )

                st.session_state.history.append(
                    f"Converted '{column}' to {new_type}."
                )

                # ==================================================
                # SAVE CHANGES
                # ==================================================  

                st.session_state.cleaned_data = data

                st.success(f"'{column}' has been converted to {new_type}.")

                st.rerun()

        except Exception:

            st.error(
               f"Cannot convert '{column}' to {new_type}. "
               "The column contains values that are not "
               "compatible with this data type." 
            ) 

            #st.divider()

    # ========================================================
    # RENAME COLUMNS
    # ========================================================

    st.divider()

    st.markdown("### ✏️ Rename Columns")

    st.caption(
        "Rename columns to improve clarity and consistency."
    )

    column = st.selectbox(
        "Select Column",
        data.columns,
        key="rename_column"
    )

    new_name = st.text_input(
        "New Column Name",
        key="new_column_name"
    )

    if st.button(
        "✏️ Rename Column",
        use_container_width=True
    ):

        if new_name.strip() == "":
            st.warning("Please enter a new column name.")

        elif new_name.strip() in data.columns:
            st.warning("This column name already exists.")

        else:

            old_name = column

            data.rename(
                columns={
                    old_name: new_name.strip()
                },
                inplace=True
            )

            st.session_state.history.append(
                f"Renamed '{old_name}' to '{new_name.strip()}'."
            )

            st.success(
                f"Column renamed from '{old_name}' to "
                f"'{new_name.strip()}'."
            )

            st.rerun()


    st.divider()

    # ========================================================
    # DROP COLUMNS
    # ========================================================

    st.markdown("### 🗑️ Drop Columns")

    st.caption("Remove unnecessary columns from your dataset.")

    columns = st.multiselect(
        "Choose Columns",
        data.columns,
        key="drop_columns"
    )

    if columns:
        st.warning(
        f"⚠️ You are about to remove {len(columns)} column(s): "
        f"{', '.join(columns)}"
        )

    if st.button(
        "🗑️ Drop Selected Columns",
        use_container_width=True
    ):

        if len(columns) == 0:

            st.warning("Please select at least one column.")

        else:

            data.drop(
                columns=columns,
                inplace=True
            )

            st.session_state.history.append(
                f"Dropped columns: {', '.join(columns)}"
            )

            st.success(
                f"Dropped {len(columns)} column(s) successfully."
            )

            st.rerun()

# ============================================================
# PAGE 6 - DATA CLEANING
# ============================================================

elif st.session_state.active_page == "Missing":

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        "<h1 style='text-align: center;'>🧩 Missing Values</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Identify and handle missing values in your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # ========================================================
    # CURRENT DATASET
    # ========================================================

    data = st.session_state.cleaned_data

    st.write("**Current Dataset**")

    rows_to_show = min(20, len(data))

    st.caption(f"Showing first {rows_to_show} of {len(data):,} rows")

    st.dataframe(data.head(20),use_container_width=True)

    st.divider()

    # ========================================================
    # MISSING VALUES
    # ========================================================

    st.subheader("⁉️ Missing Values")

    missing_values = data.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    # ========================================================
    # NO MISSING VALUES
    # ========================================================

    if missing_values.empty:

        st.success("✅ No Missing Values Found.")


    # ========================================================
    # HAS MISSING VALUES
    # ========================================================

    else:

        # ----------------------------------------------------
        # Missing Values Table
        # ----------------------------------------------------

        missing_df = missing_values.reset_index()
        missing_df.columns = ["Columns", "Missing Values"]

        # Calculate Missing Percentage
        missing_df["Missing %"] = (missing_df["Missing Values"] / len(data) * 100).round(2).astype(str) + "%"

        st.dataframe(missing_df, use_container_width=True, hide_index=True)

        total_missing = missing_values.sum()

        st.info(f"Total Missing Values : {total_missing}")

        st.divider()

        # ====================================================
        # REMOVE MISSING VALUES
        # ====================================================

        st.subheader("✂️ Remove Missing Values")

        st.write("**Select Columns**")

        missing_columns = missing_values.index.tolist()

        selected_columns = st.multiselect(
            "Choose columns to clean",
            options=missing_columns,
            key="remove_missing_columns"
        )

        st.caption(
            "⚠️ Removing missing values permanently deletes rows "
            "containing missing data."
        )

        if st.button(
            "Remove Missing Values",
            key="remove_missing_button"
        ):

            if not selected_columns:

                st.warning("Please select at least one column.")

            else:

                before = data.shape[0]

                data = data.dropna(subset=selected_columns)

                after = data.shape[0]

                removed = before - after

                if removed == 0:

                    st.info("No rows contained missing values.")

                else:

                 st.session_state.cleaned_data = data

                 st.session_state.history.append(f"Removed {removed} rows containing missing values.")

                 st.success(f"✅ Removed {removed} rows containing missing values.")

                 st.rerun()

        st.divider()

        # ====================================================
        # HANDLE MISSING VALUES
        # ====================================================

        st.subheader("🔧 Handle Missing Values")


        # ----------------------------------------------------
        # Select Columns
        # ----------------------------------------------------

        selected_columns = st.multiselect(
            "Choose columns",
            missing_columns,
            key="handle_missing_columns"
        )


        # ----------------------------------------------------
        # Method Dictionary
        # ----------------------------------------------------

        method = {}


        for col in selected_columns:

            if pd.api.types.is_numeric_dtype(data[col]):

                options = [
                    "Mean",
                    "Median",
                    "Mode"
                ]

            else:

                options = [
                    "Mode",
                    "Unknown"
                ]


            method[col] = st.selectbox(
                f"Method for {col}",
                options,
                key=f"method_{col}"
            )


            # ------------------------------------------------
            # Explanation
            # ------------------------------------------------

            if method[col] == "Mean":

                st.caption(
                    f"**{col}:** Best for normally distributed numeric data."
                )

            elif method[col] == "Median":

                st.caption(
                    f"**{col}:** Best when the data contains outliers."
                )

            elif method[col] == "Mode":

                st.caption(
                    f"**{col}:** Best when the most frequent value is suitable for the data."
                )

            elif method[col] == "Unknown":

                st.caption(
                    f"**{col}:** Fill missing values with 'Unknown'."
                )


        # ====================================================
        # HANDLE BUTTON
        # ====================================================

        if st.button(
            "Handle Missing Values",
            key="handle_missing_button"
        ):

            if not selected_columns:

                st.warning(
                    "Please select at least one column."
                )

            else:

                missing_before = data[
                    selected_columns
                ].isna().sum().sum()


                for col in selected_columns:

                    if method[col] == "Mean":

                        data[col] = data[col].fillna(
                            data[col].mean()
                        )


                    elif method[col] == "Median":

                        data[col] = data[col].fillna(
                            data[col].median()
                        )


                    elif method[col] == "Mode":

                        mode = data[col].mode()

                        if not mode.empty:

                            data[col] = data[col].fillna(
                                mode.iloc[0]
                            )


                    elif method[col] == "Unknown":

                        data[col] = data[col].fillna(
                            "Unknown"
                        )

                # ------------------------------------------------
                # Count values filled
                # ------------------------------------------------

                missing_after = data[
                    selected_columns
                ].isna().sum().sum()

                filled = missing_before - missing_after


                # Save cleaned data
                st.session_state.cleaned_data = data


                # Cleaning history
                st.session_state.history.append(
                    f"Filled {filled} missing values."
                )


                st.success(
                    f"✅ {filled} missing values filled successfully."
                )

                st.rerun()


# ============================================================
# PAGE 7 - DUPLICATES
# ============================================================

elif st.session_state.active_page == "Duplicates":

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        "<h1 style='text-align: center;'>📌 Duplicates</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Identify and remove duplicate records from your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")


    # ========================================================
    # CURRENT DATASET
    # ========================================================

    data = st.session_state.cleaned_data

    st.write("**Current Dataset**")

    rows_to_show = min(20, len(data))

    st.caption(f"Showing first {rows_to_show} of {len(data):,} rows")

    st.dataframe(data.head(20),use_container_width=True)

    st.divider()


    # ========================================================
    # DUPLICATE RECORDS
    # ========================================================

    st.subheader("📌 Duplicate Records")

    st.write("**Choose Duplicate Check Method**")


    # --------------------------------------------------------
    # SELECT CHECK METHOD
    # --------------------------------------------------------

    duplicate_method = st.radio(
        "Duplicate check method",
        [
            "Exact Duplicates (All Columns)",
            "Selected Columns"
        ],
        label_visibility="collapsed"
    )


    # ========================================================
    # OPTION 1 - EXACT DUPLICATES
    # ========================================================

    if duplicate_method == "Exact Duplicates (All Columns)":

        st.caption(
            "Checks for rows that are completely identical "
            "across all columns."
        )


        # Count duplicates
        duplicates = data.duplicated().sum()


        st.write(
            f"**Duplicate Rows:** {duplicates}"
        )


        # ----------------------------------------------------
        # NO DUPLICATES
        # ----------------------------------------------------

        if duplicates == 0:

            st.success("✅ No exact duplicate rows found.")


        # ----------------------------------------------------
        # HAS DUPLICATES
        # ----------------------------------------------------

        else:

            # Show all duplicate groups
            duplicate_data = data[
                data.duplicated(keep=False)
            ]

            st.dataframe(
                duplicate_data,
                use_container_width=True
            )


            st.divider()


            # =================================================
            # REMOVE EXACT DUPLICATES
            # =================================================

            st.subheader("✂️ Remove Duplicate Records")

            st.caption(
                "⚠️ This will permanently remove repeated rows "
                "and keep the first occurrence."
            )


            if st.button(
                "Remove Exact Duplicates",
                key="remove_exact_duplicates"
            ):

                before = len(data)


                data = data.drop_duplicates(
                    keep="first"
                )


                after = len(data)

                removed = before - after


                # Save cleaned data
                st.session_state.cleaned_data = data


                # Add history
                st.session_state.history.append(
                    f"Removed {removed} exact duplicate rows."
                )


                st.success(
                    f"✅ Removed {removed} exact duplicate rows successfully!"
                )

                st.rerun()


    # ========================================================
    # OPTION 2 - SELECTED COLUMNS
    # ========================================================

    elif duplicate_method == "Selected Columns":

        st.caption(
            "Select the columns that should be used "
            "to identify duplicate records."
        )


        # ----------------------------------------------------
        # SELECT COLUMNS
        # ----------------------------------------------------

        selected_columns = st.multiselect(
            "Choose columns to check for duplicates",
            options=data.columns.tolist(),
            key="duplicate_selected_columns"
        )


        # ----------------------------------------------------
        # CHECK SELECTED COLUMNS
        # ----------------------------------------------------

        if not selected_columns:

            st.info(
                "Please select at least one column."
            )


        else:

            # Count duplicates based on selected columns
            duplicates = data.duplicated(
                subset=selected_columns
            ).sum()


            st.write(
                f"**Duplicate Rows:** {duplicates}"
            )


            # ------------------------------------------------
            # NO DUPLICATES
            # ------------------------------------------------

            if duplicates == 0:

                st.success(
                    "✅ No duplicate rows found based on the selected columns."
                )


            # ------------------------------------------------
            # HAS DUPLICATES
            # ------------------------------------------------

            else:

                # Show all related duplicate records
                duplicate_data = data[
                    data.duplicated(
                        subset=selected_columns,
                        keep=False
                    )
                ]

                st.dataframe(
                    duplicate_data,
                    use_container_width=True
                )


                st.divider()


                # =============================================
                # REMOVE DUPLICATES
                # =============================================

                st.subheader("✂️ Remove Duplicate Records")

                st.caption(
                    "⚠️ This will permanently remove duplicate rows "
                    "based on the selected columns and keep the first occurrence."
                )


                if st.button(
                    "Remove Selected Duplicates",
                    key="remove_selected_duplicates"
                ):

                    before = len(data)


                    data = data.drop_duplicates(
                        subset=selected_columns,
                        keep="first"
                    )


                    after = len(data)

                    removed = before - after


                    # Save cleaned data
                    st.session_state.cleaned_data = data


                    # Add history
                    st.session_state.history.append(
                        f"Removed {removed} duplicate rows based on "
                        f"{', '.join(selected_columns)}."
                    )


                    st.success(
                        f"✅ Removed {removed} duplicate rows successfully!"
                    )

                    st.rerun()

# ============================================================
# PAGE 8 - OUTLIERS
# ============================================================

elif st.session_state.active_page == "Outliers":

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        "<h1 style='text-align: center;'>📈 Outliers</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Detect and manage unusual values in your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # ========================================================
    # CURRENT DATASET
    # ========================================================

    data = st.session_state.cleaned_data

    st.write("**Current Dataset**")

    rows_to_show = min(20, len(data))

    st.caption(f"Showing first {rows_to_show} of {len(data):,} rows")

    st.dataframe(data.head(20),use_container_width=True)

    st.divider()

    # ========================================================
    # OUTLIER DETECTION
    # ========================================================

    st.subheader("📈 Outlier Detection")

    numeric_columns = data.select_dtypes(
        include="number"
    ).columns


    # ========================================================
    # NO NUMERIC COLUMNS
    # ========================================================

    if len(numeric_columns) == 0:

        st.info("No numeric columns found.")


    # ========================================================
    # NUMERIC COLUMNS AVAILABLE
    # ========================================================

    else:

        # ----------------------------------------------------
        # SELECT COLUMN
        # ----------------------------------------------------

        column = st.selectbox(
            "Select Column",
            numeric_columns
        )


        # --------------------------------------------------------
        # OUTLIER CALCULATION
        # --------------------------------------------------------

        values = data[column].dropna()

        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outliers = values[
            (values < lower_bound) |
            (values > upper_bound)
        ]

        outlier_count = len(outliers)

        outlier_percentage = (
            outlier_count / len(values) * 100
            if len(values) > 0
            else 0
        )

        # ----------------------------------------------------
        # IQR INFORMATION
        # ----------------------------------------------------

        st.write("")
        st.write("**📊 IQR Information**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Q1", f"{Q1:.2f}")

        with col2:
            st.metric("Q3", f"{Q3:.2f}")

        with col3:
            st.metric("IQR", f"{IQR:.2f}")

        with col4:
            st.metric("Outliers", f"{outlier_count:,}")

        st.write("")

        # --------------------------------------------------------
        # BOUNDS
        # --------------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                f"**Lower Bound:** {lower_bound:,.2f}"
            )

        with col2:
            st.info(
                f"**Upper Bound:** {upper_bound:,.2f}"
            )

        st.write("")

        st.caption(
            f"Outlier Percentage: {outlier_percentage:.2f}%"
        )

        st.divider()

        # ----------------------------------------------------
        # DETECT OUTLIERS ROWS
        # ----------------------------------------------------

        outlier_rows = data[
            (data[column] < lower_bound) |
            (data[column] > upper_bound)
        ]


        # ----------------------------------------------------
        # OUTLIER RESULT
        # ----------------------------------------------------

        #st.write(f"Outliers Found: **{len(outliers)}**")
        st.subheader("**📌 Outlier Values**")

        if len(outliers) == 0:

            st.success(
                "✅ No outliers found in this column."
            )

        else:

            #st.caption(f"Outliers detected using the IQR method.")
            st.caption(
                f"{outlier_count:,} outlier(s) detected "
                f"using the IQR method.") 


            st.dataframe(
                outliers,
                use_container_width=True
            ) 

        # ====================================================
        # BOXPLOT
        # ====================================================

        st.divider()

        st.subheader("📦 Outlier Visualization")
        st.caption("Use the boxplot to identify the spread and potential outliers.")
        #st.caption(f"Boxplot for the '{column}' column.")

        fig, ax = plt.subplots(figsize=(10,5))

        sns.boxplot(
            y=data[column],
            ax=ax
        )

        ax.set_title(f"Boxplot of {column}")

        ax.set_ylabel(column)

        st.pyplot(fig)

        plt.close(fig)

        st.divider()


        # ====================================================
        # REMOVE OUTLIERS
        # ====================================================

        st.subheader("✂️ Remove Outliers")

        st.caption(
            f"⚠️ Removing outliers will permanently delete rows "
            f"with unusual values in the '{column}' column."
        )


        if st.button(
            "Remove Outliers",
            key="remove_outliers_button"
        ):

            before = len(data)


            # Keep non-outlier values and missing values
            data = data[
                data[column].isna() |
                data[column].between(lower_bound, upper_bound)
            ]


            after = len(data)

            removed = before - after


            # ------------------------------------------------
            # NO OUTLIERS REMOVED
            # ------------------------------------------------

            if removed == 0:

                st.info(
                    "No outliers were removed."
                )


            # ------------------------------------------------
            # OUTLIERS REMOVED
            # ------------------------------------------------

            else:

                # Save cleaned data
                st.session_state.cleaned_data = data


                # Add cleaning history
                st.session_state.history.append(
                    f"Removed {removed} outliers from '{column}'."
                )


                st.success(
                    f"✅ Successfully removed {removed:,} outlier(s) "
                    f"from '{column}'."
                )

                st.rerun()

# ============================================================
# PAGE 9 - CLEANING LOG
# ============================================================

elif st.session_state.active_page == "Cleaning Log":

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        "<h1 style='text-align: center;'>📋 Cleaning Log</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Track all cleaning operations performed on your dataset."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")


    # ========================================================
    # CLEANING HISTORY
    # ========================================================

    st.subheader("📋 Cleaning History")


    # ========================================================
    # NO CLEANING OPERATIONS
    # ========================================================

    if len(st.session_state.history) == 0:

        st.info(
            "No cleaning operations have been performed yet."
        )


    # ========================================================
    # SHOW CLEANING HISTORY
    # ========================================================

    else:

        for i, action in enumerate(
            st.session_state.history,
            start=1
        ):

            st.write(
                f"**{i}.** {action}"
            )

# ============================================================
# PAGE 10 - DOWNLOAD
# ============================================================

elif st.session_state.active_page == "Download":

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.markdown(
        "<h1 style='text-align: center;'>📥 Download</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Download your cleaned dataset for further analysis."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # ========================================================
    # CLEANED DATASET
    # ========================================================

    data = st.session_state.cleaned_data

    st.subheader("✨📄 Cleaned Dataset")

    st.caption(
        f"Your cleaned dataset contains {len(data):,} rows "
        f"and {len(data.columns):,} columns."
    )

    #st.divider()

    # --------------------------------------------------------
    # FILE FORMAT
    # --------------------------------------------------------

    file_extension = (
        st.session_state.file_name.split(".")[-1].lower()
    )

    # Get original file name
    original_file_name = st.session_state.file_name

    file_name_without_extension = original_file_name.rsplit(".", 1)[0]

    # --------------------------------------------------------
    # DOWNLOAD CSV
    # --------------------------------------------------------

    if file_extension == "csv":

        csv = data.to_csv(
            index=False
        ).encode("utf-8")

        #st.caption(f"📄 File name: {file_name_without_extension}_cleaned.csv")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name=f"{file_name_without_extension}_cleaned.csv",
            mime="text/csv",
            use_container_width=True
        )


    # --------------------------------------------------------
    # DOWNLOAD EXCEL
    # --------------------------------------------------------

    else:

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            data.to_excel(
                writer,
                index=False
            )

        #st.caption(f"📄 File name: {file_name_without_extension}_cleaned.xlsx")

        st.download_button(
            label="📥 Download Cleaned Excel",
            data=output.getvalue(),
            file_name=f"{file_name_without_extension}_cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )    


















    


    

    


                 

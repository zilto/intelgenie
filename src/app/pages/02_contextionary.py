import streamlit as st
import weaviate

import crud  # noqa


def format_contextionary_query(query: str):
    s = query.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(query) == 0:
        return query
    return s[0] + ''.join(i.capitalize() for i in s[1:])


def app():
    client = weaviate.client.Client(url="http://localhost:8080")

    st.title("Weaviate Contextionary")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Query Contextionary")
        with st.form("contextionary_query"):
            concept_query = st.text_input(label="Concept", help="Concept to query from the contextionary")
            submitted = st.form_submit_button("Query")
            if submitted:
                formatted_query = format_contextionary_query(concept_query)
                results = crud.get_contextionary_concept_vector(client, formatted_query)
                st.json(results)

    with col2:
        st.subheader("Extend Contextionary")
        with st.form("contextionary_extend"):
            concept = st.text_input(label="Concept", help="Concept:Definition pair to add to Weaviate contextionary")
            definition = st.text_area(label="Definition")
            weight = st.slider(label="Weight", min_value=0.0, max_value=1.0, value=1.0, help="'1' fully replaces old definition")

            submitted = st.form_submit_button("Extend")
            if submitted:
                crud.post_contextionary_concept(client, concept, definition, weight)
                st.success(f"'{concept}' submitted.")


if __name__ == "__main__":
    app()

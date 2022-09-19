import streamlit as st
import pandas as pd
import weaviate

import crud  # noqa


def app():
    client = weaviate.client.Client(url="http://localhost:8080")
    registry_conn = crud.connect_to_db("C:/.coding/intelgenie/data/registry.sqlite")
    registered_articles = crud.get_registry_article(registry_conn)

    df = pd.DataFrame.from_records(registered_articles)

    with st.form("Query Weaviate Semantic Search Engine"):
        col1, col2 = st.columns(2)

        with col1:
            keywords = st.text_input(label="Keyword", help="`keyword` must be present in the content")

        with col2:
            concepts = st.text_input(label="Concept", help="`concept` are semantically related to the content")

        submitted = st.form_submit_button("Search")
        if submitted:
            results = crud.gql_search_summary_dual(client, keywords, concepts)
            st.json(results)

    with st.expander("Source"):
        st.dataframe(df)


if __name__ == "__main__":
    app()

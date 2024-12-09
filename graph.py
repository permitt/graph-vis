import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

def create_cfr_knowledge_graph():
    G = nx.DiGraph()
    
    refs = {
        "§347.10": ("Active ingredients", "Referenced section containing active ingredients for skin protectant drug products"),
        "§201.66": ("Labeling format", "Format and content requirements for over-the-counter (OTC) drug product labeling"),
        "§330.1": ("General conditions", "General conditions for over-the-counter (OTC) human drugs")
    }
    for ref_id, (desc, content) in refs.items():
        G.add_node(ref_id, node_type="Applicability", label=f"{ref_id}\n{desc}", content=content)
    
    sections = {
        "§347.50": ("Definition", "Labeling requirements", 
                    "A skin protectant drug product may have more than one labeled use and labeling appropriate to different uses may be combined to eliminate duplicative words or phrases as long as the labeling is clear and understandable. When the labeling of the product contains more than one labeled use, the appropriate statement(s) of identity, indications, warnings, and directions must be stated in the labeling."),
        "(a)": ("Definition", "Statement of identity", 
                "The labeling of the product contains the established name of the drug, if any, and identifies the product with one or more of the following:"),
        "(b)": ("Information", "Indications", 
                "The labeling of the product states, under the heading \"Uses,\" one or more of the phrases listed in this paragraph (b), as appropriate. Other truthful and nonmisleading statements, describing only the uses that have been established and listed in this paragraph (b), may also be used, as provided in § 330.1(c)(2) of this chapter..."),
        "(c)": ("Information", "Warnings", 
                "The labeling of the product contains the following warnings under the heading \"Warnings\":"),
        "(d)": ("Procedure", "Directions", 
                "The labeling of the product contains the following statements, as appropriate, under the heading \"Directions\":"),
        "(e)": ("Modifier", "Lip protectant format", 
                "Products formulated and labeled as a lip protectant and that meet the criteria established in § 201.66(d)(10) of this chapter. The title, headings, subheadings, and information described in § 201.66(c) of this chapter shall be printed in accordance with the following specifications:"),
        "(f)": ("Modifier", "Basic products format", 
                "Products containing only cocoa butter, petrolatum, or white petrolatum identified in § 347.10(d), (m), and (r), singly or in combination with each other, and marketed other than as a lip protectant.")
    }
    
    for section_id, (type_, desc, content) in sections.items():
        G.add_node(section_id, node_type=type_, label=f"{section_id}\n{desc}", content=content)
        if section_id != "§347.50":
            G.add_edge("§347.50", section_id, relation="Hierarchical")
    
    subsections = {
        "(a)(1)": ("Definition", "Any product", ["§347.10"],
                   "For any product. \"Skin protectant\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(a)(2)": ("Definition", "Lip protectant", ["§347.10"],
                   "For any product formulated as a lip protectant. \"Skin protectant,\" \"lip protectant,\" or \"lip balm\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(a)(3)": ("Definition", "Poison ivy drying", ["§347.10"],
                   "For products containing any ingredient in § 347.10(b), (c), (j), (s), (t), and (u). \"Poison ivy, oak, sumac drying\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(a)(4)": ("Definition", "Poison ivy protectant", ["§347.10"],
                   "For products containing any ingredient in § 347.10(b), (c), (f), (j), (o), (s), (t), and (u). \"Poison ivy, oak, sumac protectant.\""),
        
        "(b)(1)": ("Information", "Cuts/scrapes/burns", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(b)(2)": ("Information", "Chapped skin/lips", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (g), (h), (i), (k), (l), (m), and (r)—(i) The labeling states (optional: \"helps prevent and\") \"temporarily protects\" (optional: \"and helps relieve\") (optional: \"chafed,\") \"chapped or cracked skin\" (optional: \"and lips\"). This statement may be followed by the optional statement: \"helps\" (optional: \"prevent and\") \"protect from the drying effects of wind and cold weather\". [If both statements are used, each is preceded by a bullet.]"),
        "(b)(3)": ("Information", "Poison ivy drying", ["§347.10"],
                   "For products containing any ingredient in § 347.10(b), (c), (j), (s), (t), and (u). \"Poison ivy, oak, sumac drying\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(b)(4)": ("Information", "Colloidal oatmeal", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(b)(5)": ("Information", "Sodium bicarbonate", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(b)(6)": ("Information", "Topical starch", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(b)(7)": ("Information", "Combination products", ["§347.20"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        
        "(c)(1)": ("Information", "External use", ["§201.66"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(c)(2)": ("Information", "Eye contact", [],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(c)(3)": ("Information", "Stop use", [],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(c)(4)": ("Information", "Wounds/burns", ["(b)(1)", "(b)(2)"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        
        "(d)(1)": ("Procedure", "General application", ["(b)(1)", "(b)(2)", "(b)(3)", "(b)(5)", "(b)(6)"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(d)(2)": ("Procedure", "Colloidal oatmeal", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        "(d)(3)": ("Procedure", "Sodium bicarbonate", ["§347.10"],
                   "For products containing any ingredient in § 347.10(a), (d), (e), (i), (k), (l), (m), and (r). The labeling states \"temporarily protects minor: [bullet] 1 cuts [bullet] scrapes [bullet] burns\"."),
        
        "(e)(1)": ("Modifier", "Lip format requirements", ["§201.66"],
                   "For products formulated and labeled as a lip protectant. \"Skin protectant,\" \"lip protectant,\" or \"lip balm\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(e)(2)": ("Modifier", "Lip print requirements", ["§201.66"],
                   "For products formulated and labeled as a lip protectant. \"Skin protectant,\" \"lip protectant,\" or \"lip balm\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(f)(1)": ("Modifier", "Basic format requirements", ["§201.66"],
                   "For products containing only cocoa butter, petrolatum, or white petrolatum identified in § 347.10(d), (m), and (r), singly or in combination with each other, and marketed other than as a lip protectant. \"Skin protectant,\" \"lip protectant,\" or \"lip balm\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\")."),
        "(f)(2)": ("Modifier", "Basic print requirements", ["§201.66"],
                   "For products containing only cocoa butter, petrolatum, or white petrolatum identified in § 347.10(d), (m), and (r), singly or in combination with each other, and marketed other than as a lip protectant. \"Skin protectant,\" \"lip protectant,\" or \"lip balm\" (optional, may add dosage form, e.g., \"cream,\" \"gel,\" \"lotion,\" or \"ointment\").")
    }
    
    for sub_id, (type_, desc, refs_list, content) in subsections.items():
        parent = f"({sub_id[1]})"
        G.add_node(sub_id, 
                  node_type=type_, 
                  label=f"{sub_id}\n{desc}",
                  content=content)
        G.add_edge(parent, sub_id, relation="Hierarchical")
        
        for ref in refs_list:
            if ref not in G:
                G.add_node(ref, node_type="Applicability", label=ref)
            G.add_edge(sub_id, ref, relation="References")
    
    special_relations = [
        ("(e)", "§201.66", "Requires"),
        ("(f)", "§201.66", "Requires"),
        ("(e)(1)", "§201.66", "Exempts"),
        ("(f)(1)", "§201.66", "Exempts"),
        ("(b)", "§330.1", "References"),
        ("(c)", "§201.66", "References")
    ]
    
    for source, target, relation in special_relations:
        G.add_edge(source, target, relation=relation)
    
    return G

def create_interactive_graph(G, selected_node_types=None, selected_edge_types=None):
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black",
        directed=True
    )

    color_map = {
        "Definition": "#99FF99",
        "Information": "#9999FF",
        "Procedure": "#FFFF99",
        "Modifier": "#FF99FF",
        "Applicability": "#FFB366"
    }
    edge_colors = {
        "Hierarchical": "#404040",
        "References": "#FFA500",
        "Requires": "#0000FF",
        "Exempts": "#00FF00"
    }

    # Add nodes
    for node in G.nodes():
        node_type = G.nodes[node].get('node_type', 'Default')
        if selected_node_types is None or node_type in selected_node_types:
            net.add_node(
                node,
                label=G.nodes[node].get('label', node),
                color=color_map.get(node_type, "#CCCCCC"),
                title=G.nodes[node].get('content', ''),
                node_type=node_type,
                content=G.nodes[node].get('content', '')
            )

    # Add edges
    for edge in G.edges():
        relation = G.edges[edge].get('relation', 'Default')
        if selected_edge_types is None or relation in selected_edge_types:
            net.add_edge(
                edge[0],
                edge[1],
                color=edge_colors.get(relation, "#CCCCCC"),
                title=relation
            )

    net.set_options("""
    {
        "nodes": {
            "shape": "box",
            "font": {
                "size": 12,
                "face": "arial"
            }
        },
        "edges": {
            "smooth": true
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "iterations": 100
            },
            "repulsion": {
                "centralGravity": 0.1,
                "springLength": 120,
                "springConstant": 0.05,
                "nodeDistance": 150,
                "damping": 0.09
            },
            "solver": "repulsion"
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
        }
    }
    """)

    html_content = net.generate_html()

    html_content = html_content.replace(
        "var network = new vis.Network(container, data, options);",
        "var network = new vis.Network(container, data, options);\nwindow.visNetwork = network;"
    )

    click_handler = """
    <script>
    window.parent.postMessage(nodeData, "*");
    function initNetwork() {
        console.log("ALO RODJACE");
        // Poll until network is available
        const checkNetwork = setInterval(() => {
            if (window.visNetwork) {
                clearInterval(checkNetwork);
                const network = window.visNetwork;
                network.on("click", function(params) {
                    console.log("Click event:", params);
                    if (params.nodes.length > 0) {
                        const nodeId = params.nodes[0];
                        const node = network.body.nodes[nodeId];
                        if (node) {
                            const nodeData = {
                                type: node.options.node_type,
                                section: nodeId,
                                content: node.options.title
                            };
                            if (window.Streamlit) {
                                window.Streamlit.setComponentValue(nodeData);
                            }
                        }
                    }
                });
            }
        }, 100);

        setTimeout(() => clearInterval(checkNetwork), 10000);
    }
    window.addEventListener('load', initNetwork);
    </script>
    """

    html_content = html_content.replace('</body>', click_handler + '</body>')
    html_content = html_content.replace('<script src="lib/bindings/utils.js"></script>', '')

    return html_content

def main():
    st.title("CFR Section 347.50 Interactive Knowledge Graph")

    col1, col2 = st.columns([3, 1])

    with st.sidebar:
        st.header("Node Details")
        st.write("Click on a node to view details")

        st.subheader("Filters")
        node_types = ["Definition", "Information", "Procedure", "Modifier", "Applicability"]
        selected_node_types = st.multiselect(
            "Filter by Node Type",
            node_types,
            default=node_types
        )

        edge_types = ["Hierarchical", "References", "Requires", "Exempts"]
        selected_edge_types = st.multiselect(
            "Filter by Edge Type",
            edge_types,
            default=["Hierarchical", "References"]
        )

        st.markdown("### Legend")
        st.markdown("""
        **Node Types:**
        - 🟢 Definition (Green)
        - 🔵 Information (Blue)
        - 🟡 Procedure (Yellow)
        - 🟣 Modifier (Pink)
        - 🟠 Applicability (Orange)

        **Edge Types:**
        - ⚫ Hierarchical (Gray)
        - 🟠 References (Orange)
        - 🔵 Requires (Blue)
        - 🟢 Exempts (Green)
        """)

        if "component_value" in st.session_state:
            details = st.session_state["component_value"]
            st.markdown("---")
            st.markdown(f"### Selected Node: {details.get('section', '')}")
            st.markdown(f"**Type:** {details.get('type', '')}")
            st.markdown(f"**Content:**\n{details.get('content', '')}")

    G = create_cfr_knowledge_graph()

    with col1:
        with st.spinner("Generating visualization..."):
            html_content = create_interactive_graph(G, selected_node_types, selected_edge_types)
            components.html(
                html_content,
                height=800,
                width=800
            )

if __name__ == "__main__":
    main()

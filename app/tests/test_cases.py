from app.main import *


def test_interpret_pricat():
    input = """article_number;size;color;empty_field
15189-02-001;36;white;
15189-02-001;37;white;
15189-02-001;38;black;"""

    result = interpret_pricat(file=input)

    variants = [
        {"article_number": "15189-02-001", "size": "36", "color": "white", "empty_field": ""},
        {"article_number": "15189-02-001", "size": "37", "color": "white", "empty_field": ""},
        {"article_number": "15189-02-001", "size": "38", "color": "black", "empty_field": ""},
    ]
    assert result == variants


def test_interpret_mapping():
    input = """source;destination;source_type;destination_type
36|white;36 white;size|color;size&color
37|white;37 white;size|color;size&color
38|black;38 black;size|color;size&color"""

    result = interpret_mapping(file=input)
    print(result)

    assert result == [
        {
            SOURCE: ["36", "white"],
            DESTINATION: "36 white",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
        {
            SOURCE: ["37", "white"],
            DESTINATION: "37 white",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
        {
            SOURCE: ["38", "black"],
            DESTINATION: "38 black",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
    ]


def test_apply_mapping():
    mapping = [
        {
            SOURCE: ["36", "white"],
            DESTINATION: "36 white",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
        {
            SOURCE: ["37", "white"],
            DESTINATION: "37 white",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
        {
            SOURCE: ["38", "black"],
            DESTINATION: "38 black",
            SOURCE_TYPE: ["size", "color"],
            DESTINATION_TYPE: "size&color",
        },
    ]
    unmapped_variants = [
        {"article_number": "15189-02-001", "size": "36", "color": "white", "empty_field": ""},
        {"article_number": "15189-02-001", "size": "37", "color": "white", "empty_field": ""},
        {"article_number": "15189-02-001", "size": "38", "color": "black", "empty_field": ""},
    ]

    result = apply_mapping(mapping=mapping, unmapped_variations=unmapped_variants)

    assert result == [
        {"article_number": "15189-02-001", "size&color": "36 white"},
        {"article_number": "15189-02-001", "size&color": "37 white"},
        {"article_number": "15189-02-001", "size&color": "38 black"},
    ]


def test_group_articles():
    variations = [
        {"article_number": "15189-02-001", "size": "36", "color": "white"},
        {"article_number": "15189-02-001", "size": "37", "color": "white"},
        {"article_number": "15189-02-002", "size": "38", "color": "black"},
    ]

    result = group_articles(variations)

    assert result == [
        {
            "article_number": "15189-02-001",
            VARIATIONS: [{"size": "36", "color": "white"}, {"size": "37", "color": "white"}],
        },
        {
            "article_number": "15189-02-002",
            VARIATIONS: [{"size": "38", "color": "black"}],
        },
    ]


def test_move_variant_attributes_up():
    articles = [
        {
            "article_number": "15189-02-001",
            VARIATIONS: [{"size": "36", "color": "white"}, {"size": "37", "color": "white"}],
        },
        {
            "article_number": "15189-02-002",
            VARIATIONS: [{"size": "38", "color": "black"}],
        },
    ]

    result = move_variant_attributes_up(articles)
    print(json.dumps(result, indent=2))

    assert result == [
        {
            "article_number": "15189-02-001",
            "color": "white",
            VARIATIONS: [{"size": "36"}, {"size": "37"}],
        },
        {
            "article_number": "15189-02-002",
            "size": "38",
            "color": "black",
            VARIATIONS: [{}],
        },
    ]


def test_move_article_attributes_up():
    articles = [
        {
            "article_number": "15189-02-001",
            "color": "white",
            "brand": "fashion cloud",
            VARIATIONS: [{"size": "36"}, {"size": "37"}],
        },
        {
            "article_number": "15189-02-002",
            "size": "38",
            "color": "black",
            "brand": "fashion cloud",
            VARIATIONS: [{}],
        },
    ]

    result = move_article_attributes_up(articles)

    assert result == {
        "brand": "fashion cloud",
        ARTICLES: [
            {
                "article_number": "15189-02-001",
                "color": "white",
                VARIATIONS: [{"size": "36"}, {"size": "37"}],
            },
            {
                "article_number": "15189-02-002",
                "size": "38",
                "color": "black",
                VARIATIONS: [{}],
            },
        ],
    }

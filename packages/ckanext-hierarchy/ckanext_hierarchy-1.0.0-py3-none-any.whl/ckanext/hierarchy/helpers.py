import ckan.plugins.toolkit as tk
import ckan.model as model

CONFIG_TREE_SEARCH_EDNPOINTS = "ckanext.hierarchy.tree_search_endpoints"
DEFAULT_TREE_SEARCH_ENDPOINTS = "organization.read"


def get_helpers():
    return {
        "group_tree": group_tree,
        "group_tree_section": group_tree_section,
        "group_tree_parents": group_tree_parents,
        "group_tree_get_longname": group_tree_get_longname,
        "group_tree_highlight": group_tree_highlight,
        "get_allowable_parent_groups": get_allowable_parent_groups,
        "hierarchy_enable_tree_search": hierarchy_enable_tree_search,
    }


def group_tree(organizations=[], type_="organization"):
    full_tree_list = tk.get_action("group_tree")({}, {"type": type_})

    if not organizations:
        return full_tree_list
    else:
        filtered_tree_list = group_tree_filter(organizations, full_tree_list)
        return filtered_tree_list


def group_tree_filter(organizations, group_tree_list, highlight=False):
    # this method leaves only the sections of the tree corresponding to the
    # list since it was developed for the users, all children organizations
    # from the organizations in the list are included
    def traverse_select_highlighted(group_tree, selection=[], highlight=False):
        # add highlighted branches to the filtered tree
        if group_tree["highlighted"]:
            # add to the selection and remove highlighting if necessary
            if highlight:
                selection += [group_tree]
            else:
                selection += group_tree_highlight([], [group_tree])
        else:
            # check if there is any highlighted child tree
            for child in group_tree.get("children", []):
                traverse_select_highlighted(child, selection)

    filtered_tree = []
    # first highlights all the organizations from the list in the three
    for group in group_tree_highlight(organizations, group_tree_list):
        traverse_select_highlighted(group, filtered_tree, highlight)

    return filtered_tree


def group_tree_section(
    id_, type_="organization", include_parents=True, include_siblings=True
):
    return tk.get_action("group_tree_section")(
        {
            "include_parents": include_parents,
            "include_siblings": include_siblings,
        },
        {
            "id": id_,
            "type": type_,
        },
    )


def group_tree_parents(id_, type_="organization"):
    tree_node = tk.get_action("organization_show")({}, {"id": id_})
    if tree_node["groups"]:
        parent_id = tree_node["groups"][0]["name"]
        parent_node = tk.get_action("organization_show")({}, {"id": parent_id})
        return group_tree_parents(parent_id) + [parent_node]
    else:
        return []


def group_tree_get_longname(id_, default="", type_="organization"):
    tree_node = tk.get_action("organization_show")({}, {"id": id_})
    longname = tree_node.get("longname", default)
    if not longname:
        return default
    return longname


def group_tree_highlight(organizations, group_tree_list):
    def traverse_highlight(group_tree, name_list):
        group_tree["highlighted"] = group_tree.get("name", "") in name_list

        for child in group_tree.get("children", []):
            traverse_highlight(child, name_list)

    selected_names = [o.get("name", None) for o in organizations]

    for group in group_tree_list:
        traverse_highlight(group, selected_names)
    return group_tree_list


def get_allowable_parent_groups(group_id=None):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = group.groups_allowed_to_be_its_parent(
            type="organization"
        )
    else:
        allowable_parent_groups = model.Group.all(group_type="organization")
    return allowable_parent_groups


def hierarchy_enable_tree_search():
    endpoint = ".".join(tk.get_endpoint())
    supported_endpoints = tk.aslist(
        tk.config.get(
            CONFIG_TREE_SEARCH_EDNPOINTS, DEFAULT_TREE_SEARCH_ENDPOINTS
        )
    )
    return endpoint in supported_endpoints

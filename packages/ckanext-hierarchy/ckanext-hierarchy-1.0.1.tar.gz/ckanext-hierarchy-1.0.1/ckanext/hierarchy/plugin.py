import logging

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan import model

from ckanext.hierarchy.logic import action
from ckanext.hierarchy import helpers

log = logging.getLogger(__name__)


class HierarchyPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_public_directory(config, "assets")
        tk.add_resource("assets", "hierarchy")

    # IActions

    def get_actions(self):
        return action.get_actions()

    # ITemplateHelpers
    def get_helpers(self):
        return helpers.get_helpers()

    # IPackageController

    def before_search(self, search_params):
        """When searching an organization, optionally extend the search any
        sub-organizations too. This is achieved by modifying the search options
        before they go to SOLR.
        """
        if not tk.h.hierarchy_enable_tree_search():
            return search_params

        if "ext_hierarchy_enable_tree_search" not in tk.request.params:
            return search_params

        fq = search_params.get("fq")

        group = model.Group.get(tk.request.view_args["id"])
        if not group:
            return search_params

        children_org_hierarchy = group.get_children_group_hierarchy(type="organization")
        children_names = [org[1] for org in children_org_hierarchy]

        if children_names:
            # remove existing owner_org:"<parent>" clause - we'll replace
            # it with the tree of orgs in a moment.
            owner_org_q = 'owner_org:"{}"'.format(group.id)
            expanded_org_q = "organization:({})".format(
                " OR ".join(
                    org_name
                    for org_name in [group.name]
                    + children_names
                )
            )

            search_params["fq"] = fq.replace(owner_org_q, expanded_org_q)

        return search_params

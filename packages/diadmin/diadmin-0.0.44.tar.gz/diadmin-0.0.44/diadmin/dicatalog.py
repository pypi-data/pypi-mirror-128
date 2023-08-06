
import logging
import argparse
from urllib.parse import urljoin

import yaml
import json
from os.path import join

from diadmin.metadata_api import catalog
from diadmin.utils.utils import add_defaultsuffix

def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    description =  "Export and import catalog hierarchies."
    parser = argparse.ArgumentParser(description=description)
    help_config = 'Specifies config_demo.yaml file with the parameters: URL, TENANT, USER, PWD'
    parser.add_argument('hierarchy', help = "Hierarchy name in DI for export or json-file for import.")
    parser.add_argument('-e','--export_catalog', help='Exports hierarchy',action='store_true')
    parser.add_argument('-i','--import_catalog', help='Imports hierarchy',action='store_true')
    parser.add_argument('-c','--config', help = help_config,default='config.yamls')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = add_defaultsuffix(args.config,'yaml')

    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    conn = {'url': urljoin(params['URL'] , '/app/datahub-app-metadata'),
            'auth':(params['TENANT']+'\\'+ params['USER'],params['PWD'])}
    catalog_directory = 'catalogs'

    if args.export_catalog :
        hnames = catalog.get_hierarchy_names(conn, search=args.hierarchy)
        if hnames :
            hierarchy = catalog.get_hierarchy_tags(conn, hnames['tagHierarchies'][0]["tagHierarchy"]['id'])
            catalog_file = join(catalog_directory,args.hierarchy + ".json")
            with open(catalog_file,'w') as fp:
                json.dump(hierarchy,fp = fp,indent=4)
        else :
            logging.error(f'Hierarchy not found: {args.hierarchy}')

    if args.import_catalog :

        hfile = add_defaultsuffix(args.hierarchy,'json')
        with open(join(catalog_directory, hfile)) as fp:
            hierarchy = json.load(fp)

        hierarchy = catalog.convert_standard_hierarchy(hierarchy)
        catalog.add_path_id_list(hierarchy)
        catalog.upload_hierarchy(conn,hierarchy)



if __name__ == '__main__':
    main()
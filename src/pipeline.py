import json
import logging
from .adapters.comsol_adapter import COMSOLAdapter
from .adapters.process_adapter import process
from .adapters.origin_adapter import OriginAdapter


def dry_run(c):
    print(json.dumps({k:v for k,v in c.items() if not k.startswith('_')},ensure_ascii=False,indent=2,default=str))
    print('DRY RUN: no COMSOL/Origin connection, data extraction or output generation.')


def list_results(c):
    if c['comsol']['mode']!='mph':
        from .exceptions import ConfigError
        raise ConfigError('--list-results requires [comsol].mode = "mph".')
    adapter=COMSOLAdapter(c)
    try:
        for item in adapter.list_available_results():
            print(f'{item["kind"]:8s} {item["tag"]:16s} {item["label"]}')
    finally:
        adapter.close()


def run(c):
    log=logging.getLogger('pipeline')
    comsol=COMSOLAdapter(c)
    origin=OriginAdapter(c)
    try:
        dataset=comsol.extract_dataset()
        dataset=process(dataset,c)
        path=c['paths']['processed_file']
        dataset.data.to_csv(path,index=False,encoding='utf-8-sig')
        path.with_suffix('.metadata.json').write_text(json.dumps({
            'name':dataset.name,'source':dataset.source,'variables':dataset.variables,
            'units':dataset.units,'metadata':dataset.metadata},ensure_ascii=False,indent=2,default=str),encoding='utf-8')
        origin.connect()
        book=origin.write_dataframe(dataset)
        graph=origin.create_graph(book,dataset)
        figure=origin.export_graph(graph)
        project=origin.save_project()
        origin.success=True
        log.info('Pipeline completed. Figure: %s; Project: %s',figure,project)
        return dataset,figure,project
    finally:
        origin.close()
        comsol.close()

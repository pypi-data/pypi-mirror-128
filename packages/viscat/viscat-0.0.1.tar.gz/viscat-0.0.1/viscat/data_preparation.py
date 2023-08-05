import os
import pandas as pd

INDICIES = ['CREATE INDEX patientId FOR (p:Patient) ON (p.patientId);',
            'CREATE INDEX conceptId FOR (c:Concept) ON (c.conceptId);',
            'CREATE INDEX documentId FOR (d:Document) ON (d.documentId);']

def create_neo_csv(data, columns, output_dir='/etc/lib/neo4j/import/',
                   base_name='patients'):
    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data
        columns:
            What data to use from the dataframe
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
        base_name:
            Name of the csv
    '''
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        df = pd.read_csv(data)

    # Remove duplicates
    df = df.drop_duplicates(subset=columns)

    out_df = df[columns]
    data_path = os.path.join(output_dir, f"{base_name}.csv")
    out_df.to_csv(data_path, index=False)


def create_patients_csv(data, output_dir='/etc/lib/neo4j/import/',
                        base_name='patients'):
    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: patientId
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible,
            but writing there could be only admin
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'CREATE (:Patient {patientId: toString(row.patientId)}) '
        )

    create_neo_csv(data=data, columns=['patientId'],
                   output_dir=output_dir, base_name=base_name)

    return query


def create_documents_csv(data, output_dir='/etc/lib/neo4j/import/',
                         base_name='documents'):
    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: documentId
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'CREATE (:Document {documentId: toString(row.documentId)}) '
        )

    create_neo_csv(data=data, columns=['documentId'],
                   output_dir=output_dir, base_name=base_name)

    return query


def create_concepts_csv(data, output_dir='/etc/lib/neo4j/import/',
                         base_name='concepts'):
    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: conceptId,
            name and type
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'CREATE (:Concept {conceptId: toString(row.conceptId), '
        '                  type: toString(row.type), '
        '                  name: toString(row.name)}) '
        )

    create_neo_csv(data=data, columns=['conceptId', 'name', 'type'],
                   output_dir=output_dir, base_name=base_name)

    return query


def create_document2patient_csv(data, output_dir='/etc/lib/neo4j/import/',
                                base_name='document2patient'):

    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: patientId and
            documentId
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'MATCH (pt:Patient {patientId: toString(row.patientId)}) '
        'MATCH (doc:Document {documentId: toString(row.documentId)}) '
        'CREATE (pt)-[:HAS]->(doc); '
        )

    create_neo_csv(data=data, columns=['patientId', 'documentId'],
                   output_dir=output_dir, base_name=base_name)

    return query


def create_concept_ontology_csv(data, output_dir='/etc/lib/neo4j/import/',
                                base_name='concept_ontology'):

    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: child, parent
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'MATCH (child:Concept {conceptId: toString(row.child)}) '
        'MATCH (parent:Concept {conceptId: toString(row.parent)}) '
        'CREATE (child)-[:IS_A]->(parent); '
        )

    create_neo_csv(data=data, columns=['child', 'parent'],
                   output_dir=output_dir, base_name=base_name)

    return query


def create_document2concept_csv(data, output_dir='/etc/lib/neo4j/import/',
                         base_name='document2concepts'):
    r''' Creates a patients CSV for neo4j load csv function

    Args:
        data:
            A dataframe or path to a dataframe with the required data: 'conceptId',
            'documentId', 'contextSimilarity', 'start', 'end', 'timestamp',
            'metaSubject', 'metaPresence', 'metaTime'
        output_dir:
            Where to save the CSVs, should be the neo4j imports path if possible
    '''
    query = (
        'USING PERIODIC COMMIT 100000 '
        f'LOAD CSV WITH HEADERS FROM  "file:///{base_name}.csv" AS row '
        'MATCH (doc:Document{documentId: toString(row.documentId)}) '
        'MATCH (concept:Concept {conceptId: toString(row.conceptId)}) '
        'CREATE (doc)-[:HAS {start: toInteger(row.start), '
        '                   end: toInteger(row.end), '
        '                   timestamp: toInteger(row.timestamp), '
        '                   contextSimilarity: toFloat(row.contextSimilarity), '
        '                   metaSubject: toString(row.metaSubject), '
        '                   metaPresence: toString(row.metaPresence), '
        '                   metaTime: toString(row.metaTime) '
        '            }]->(concept);'
        )

    columns = ['conceptId', 'documentId', 'contextSimilarity', 'start',
                'end', 'timestamp', 'metaSubject', 'metaPresence', 'metaTime']

    create_neo_csv(data=data, columns=columns,
                   output_dir=output_dir, base_name=base_name)

    return query


def get_data_from_docs(docs, doc2pt, doc2time=None):
    data = [['conceptId', 'documentId', 'contextSimilarity',
             'start', 'end', 'timestamp', 'metaSubject',
             'metaPresence', 'metaTime']]

    for doc_id, doc in docs.items():
        row = []
        for ent in doc['entities'].values():
            #if ent['meta_anns']['Subject']['value'] == 'Patient' and \
            #   ent['meta_anns']['Presence']['value'] == 'True':
            if doc2time is not None:
                t = doc2time[doc_id]
            else:
                t = ent['document_timestamp']

            row = [ent['cui'], doc_id,
                   ent['context_similarity'],
                   ent['start'], ent['end'],
                   t,
                   ent['meta_anns']['Subject']['value'],
                   ent['meta_anns']['Presence']['value'],
                   ent['meta_anns']['Time']['value']]
            data.append(row)
            row = []

    return data

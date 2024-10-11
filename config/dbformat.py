import json

class Dbformat:
    def db_format(self, columns = list, db = list) -> dict:
        formated = {column: [] for column in columns}

        try:
            for result in db:
                for ind, column in enumerate(columns):
                    formated[column].append(result[ind])
            
        
        except Exception as error:
            raise error
        

        return formated
    
    def db_format_to_geojson(self, dbformat = dict, geometry = str):
        geojson = {
                    "type": "FeatureCollection",
                    "features": []
                }

        for ind, item in enumerate(dbformat[next(iter(dbformat))]):
            feature = {
                'type':'Feature',
                'geometry': json.loads(dbformat[geometry][ind]),
                'properties': {}
            }

            for column in dbformat.keys():
                if column == geometry:
                    pass
                else:
                    feature['properties'][column] = dbformat[column][ind]

            geojson['features'].append(feature)

        return geojson

            

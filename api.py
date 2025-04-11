from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import requests
import json
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
cors = CORS(app)


@app.get('/rest-v1/historical_cities')
def historical_cities_data():
    city_list = []

    if request.args.get('city'):
        city = request.args.get('city').strip().replace('"', '').lower()
    else:
        city = None
    
    if ',' in (request.args.get('marker', 'Built Heritage')):
        marker_param = request.args.get('marker', 'Built Heritage')
        marker = [m.strip().replace('"','').lower() for m in marker_param.split(',')]    
    else:
        marker = [request.args.get('marker', 'Built Heritage').strip().replace('"','').lower()]

    if city is None:
        try:
            response = requests.get('https://icvtesting.nvli.in/rest-v1/historic-cities', verify=False)
            if response.status_code == 200:
                data = json.loads(response.text)['results']
                
                for city in data:
                    city_obj = {}
                    city_obj['nid'] = city['nid']
                    city_obj['title'] = city['title']
                    city_obj['field_hc_thumbnails'] = city['field_hc_thumbnails']
                    city_obj['field_hc_city_capsule_images'] = city['field_hc_city_capsule_images']
                    city_obj['field_hc_city_capsule_redirect_l'] = city['field_hc_city_capsule_redirect_l']
                    city_obj['field_historic_cities_introducti'] = city['field_historic_cities_introducti']
                    city_obj['field_hc_app_timeline_link'] = city['field_hc_app_timeline_link']
                    city_obj['field_historic_cities_city_tales'] = city['field_historic_cities_city_tales']
                    city_obj['field_historic_cities_history'] = city['field_historic_cities_history']
                    city_obj['field_histroric_city_city_tales'] = city['field_histroric_city_city_tales']
                    city_obj['field_map_image'] = city['field_map_image']
                    city_obj['field_history_timeline_code'] =city['field_history_timeline_code']
                    city_obj['field_city_tales_links'] = city['field_city_tales_links']
                    city_list.append(city_obj)
                return jsonify({"results":city_list}) 
        except Exception as e:
            print(e)
            return jsonify({"results": "Could not fetch data from historical data API. Try Again!"}), 400
        
    else:
        print(city, marker)
        filtered_output = []

        try:
            response = requests.get('https://icvtesting.nvli.in/rest-v1/historic-cities', verify=False)
            if response.status_code == 200:
                data = json.loads(response.text)['results']
            
            if city not in ["varanasi"]:
                for hist_city in data:
                    if str(hist_city['title'].lower()) == str(city.strip().lower()):
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:
                            city_object = {}

                            cleaned_data = hist_city_item.replace('[', '')
                            len_split_data = (len(cleaned_data.split('},')))

                            if len_split_data == 1:
                                if cleaned_data.split('},')[-1].lstrip(',') != '':
                                    cleaned_data_final = json.loads(cleaned_data.split('},')[-1].lstrip(','))
                                    for marker_item in marker:
                                        if cleaned_data_final['field_pin_type'].lower() == marker_item:
                                            city_object['nid'] = cleaned_data_final['nid']
                                            city_object['title'] = cleaned_data_final['title']
                                            city_object['field_marker_introduction_image'] = cleaned_data_final['field_marker_introduction_image']
                                            city_object['field_marker_link_text'] = cleaned_data_final['field_marker_link_text']
                                            city_object['field_pin_type'] = cleaned_data_final['field_pin_type']
                                            city_object['field_marker_slide_image'] = cleaned_data_final['field_marker_slide_image']
                                            city_object['field_video_path'] = cleaned_data_final['field_video_path']
                                            city_object['field_tabname'] = cleaned_data_final['field_tabname']
                                            city_object['field_marker_description'] = cleaned_data_final['field_marker_description']
                                            city_object['field_video_note'] = cleaned_data_final['field_video_note']
                                            city_object['field_audio_path'] = cleaned_data_final['field_audio_path']
                                            city_object['field_document_title'] = cleaned_data_final['field_document_title']
                                            city_object['field_node_id'] = cleaned_data_final['field_node_id']
                                            city_object['field_marker_introduction'] = cleaned_data_final['field_marker_introduction']
                                            city_object['field_pin_position_x'] = cleaned_data_final['field_pin_position_x']
                                            city_object['field_pin_position_y'] = cleaned_data_final['field_pin_position_y']
                                            filtered_output.append(city_object)     

                            else:
                                data = (cleaned_data.split('},')[0])
                                data = data.lstrip(',')
                                data = data + '}'
                                data = json.loads(data)
                
                                for marker_item in marker:
                                    print(marker_item.lower())
                                    if data['field_pin_type'] == marker_item.lower():
                                        city_object['nid'] = data['nid']
                                        city_object['title'] = data['title']
                                        city_object['field_marker_introduction_image'] = data['field_marker_introduction_image']
                                        city_object['field_marker_link_text'] = data['field_marker_link_text']
                                        city_object['field_pin_type'] = data['field_pin_type']
                                        city_object['field_marker_slide_image'] = data['field_marker_slide_image']
                                        city_object['field_video_path'] = data['field_video_path']
                                        city_object['field_tabname'] = data['field_tabname']
                                        city_object['field_marker_description'] = data['field_marker_description']
                                        city_object['field_video_note'] = data['field_video_note']
                                        city_object['field_audio_path'] = data['field_audio_path']
                                        city_object['field_document_title'] = data['field_document_title']
                                        city_object['field_node_id'] = data['field_node_id']
                                        city_object['field_marker_introduction'] = data['field_marker_introduction']
                                        city_object['field_pin_position_x'] = data['field_pin_position_x']
                                        city_object['field_pin_position_y'] = data['field_pin_position_y']
                                        filtered_output.append(city_object)                    
                return ({"results": filtered_output}), 200
            
           
            if city == 'varanasi':
                for hist_city in data:
                    if hist_city['title'].lower().strip() == 'varanasi':
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:
                            data = hist_city_item.lstrip(',')
                            if data != '':
                                data_json = (json.loads(data + ']')) 
                                data_json = data_json[0]
                                for marker_item in marker:
                                    if data_json['field_pin_type'].lower() == marker_item:
                                        varanasi_city_obj = {}
                                        varanasi_city_obj['nid'] = data_json['nid']
                                        varanasi_city_obj['title'] = data_json['title']
                                        varanasi_city_obj['field_marker_introduction_image'] = data_json['field_marker_introduction_image']
                                        varanasi_city_obj['field_marker_link_text'] = data_json['field_marker_link_text']
                                        varanasi_city_obj['field_pin_type'] = data_json['field_pin_type']
                                        varanasi_city_obj['field_marker_slide_image'] = data_json['field_marker_slide_image']
                                        varanasi_city_obj['field_video_path'] = data_json['field_video_path']
                                        varanasi_city_obj['field_tabname'] = data_json['field_tabname']
                                        varanasi_city_obj['field_marker_description'] = data_json['field_marker_description']
                                        varanasi_city_obj['field_video_note'] = data_json['field_video_note']
                                        varanasi_city_obj['field_audio_path'] = data_json['field_audio_path']
                                        varanasi_city_obj['field_document_title'] = data_json['field_document_title']
                                        varanasi_city_obj['field_node_id'] = data_json['field_node_id']
                                        varanasi_city_obj['field_marker_introduction'] = data_json['field_marker_introduction']
                                        varanasi_city_obj['field_pin_position_x'] = data_json['field_pin_position_x']
                                        varanasi_city_obj['field_pin_position_y'] = data_json['field_pin_position_y']
                                        filtered_output.append(varanasi_city_obj)
                        return jsonify({"results": filtered_output})                  
        except Exception as e:
            print(e)


app.run(debug=True)

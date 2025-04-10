from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import requests
import json
import ast
from collections import OrderedDict
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
cors = CORS(app)


@app.get('/rest-v1/historical_cities')
def historical_city_info():
    city_list = []

    if request.args.get('city'):
        city = request.args.get('city').strip().replace('"', '')
    else:
        city = None
    
    if ',' in (request.args.get('marker', 'Built Heritage')):
        marker_param = request.args.get('marker', 'Built Heritage')
        marker = [m.strip().replace('"','') for m in marker_param.split(',')]    
    else:
        marker = [request.args.get('marker', 'Built Heritage').strip().replace('"','')]

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
        
        for hist_city in data:
            # print(hist_city['title'], city, hist_city['title']==city)
            if str(hist_city['title'].lower()) == str(city.strip().lower()):
                hist_city_data_list = hist_city['field_markers'].split(']')
                for hist_city_item in hist_city_data_list:
                    city_object = {}
                    cleaned_data = hist_city_item.replace('[', '')
                    cleaned_data = cleaned_data.lstrip(',')
                    cleaned_data = cleaned_data.replace("'", '"')

                    # special case for kolkata. Was not parsing json
                    if 'Kolkata' in cleaned_data:
                        kolkata_data_list = cleaned_data.split('}')

                        for kolkata_cleaned_data in kolkata_data_list:
                            if kolkata_cleaned_data != '':
                                kolkata_cleaned_data = kolkata_cleaned_data.lstrip(',')
                                kolkata_cleaned_data = kolkata_cleaned_data + '}'

                                if kolkata_cleaned_data != '':
                                    kolkata_cleaned_data_dumped = json.dumps(kolkata_cleaned_data, indent=2)
                                    kolkata_cleaned_data_dict = json.loads(kolkata_cleaned_data_dumped)
                                    kolkata_cleaned_data_dict = json.loads(kolkata_cleaned_data_dict)

                
                                    for marker_item in marker:
                                        # print(kolkata_cleaned_data_dict['field_pin_type'])
                                        if kolkata_cleaned_data_dict['field_pin_type'] == marker_item:
                                            city_object['nid'] = kolkata_cleaned_data_dict['nid']
                                            city_object['title'] = kolkata_cleaned_data_dict['title']
                                            city_object['field_marker_introduction_image'] = kolkata_cleaned_data_dict['field_marker_introduction_image']
                                            city_object['field_marker_link_text'] = kolkata_cleaned_data_dict['field_marker_link_text']
                                            city_object['field_pin_type'] = kolkata_cleaned_data_dict['field_pin_type']
                                            city_object['field_marker_slide_image'] = kolkata_cleaned_data_dict['field_marker_slide_image']
                                            city_object['field_video_path'] = kolkata_cleaned_data_dict['field_video_path']
                                            city_object['field_tabname'] = kolkata_cleaned_data_dict['field_tabname']
                                            city_object['field_marker_description'] = kolkata_cleaned_data_dict['field_marker_description']
                                            city_object['field_video_note'] = kolkata_cleaned_data_dict['field_video_note']
                                            city_object['field_audio_path'] = kolkata_cleaned_data_dict['field_audio_path']
                                            city_object['field_document_title'] = kolkata_cleaned_data_dict['field_document_title']
                                            city_object['field_node_id'] = kolkata_cleaned_data_dict['field_node_id']
                                            city_object['field_marker_introduction'] = kolkata_cleaned_data_dict['field_marker_introduction']
                                            city_object['field_pin_position_x'] = kolkata_cleaned_data_dict['field_pin_position_x']
                                            city_object['field_pin_position_y'] = kolkata_cleaned_data_dict['field_pin_position_y']
                                            filtered_output.append(city_object)
                        return ({"results": filtered_output}), 200

                    # special case for Bhopal. Unable to parse json
                    if 'Bhopal' in cleaned_data:
                        cleaned_bhopal_data = json.dumps(cleaned_data, indent=2)
                        if cleaned_bhopal_data != '':
                            cleaned_bhopal_dict = json.loads(cleaned_bhopal_data)
                            cleaned_bhopal_dict = json.loads(cleaned_bhopal_dict)
                            for marker_item in marker:
                                if cleaned_bhopal_dict['field_pin_type'] == marker_item:
                                    city_object['nid'] = cleaned_bhopal_dict['nid']
                                    city_object['title'] = cleaned_bhopal_dict['title']
                                    city_object['field_marker_introduction_image'] = cleaned_bhopal_dict['field_marker_introduction_image']
                                    city_object['field_marker_link_text'] = cleaned_bhopal_dict['field_marker_link_text']
                                    city_object['field_pin_type'] = cleaned_bhopal_dict['field_pin_type']
                                    city_object['field_marker_slide_image'] = cleaned_bhopal_dict['field_marker_slide_image']
                                    city_object['field_video_path'] = cleaned_bhopal_dict['field_video_path']
                                    city_object['field_tabname'] = cleaned_bhopal_dict['field_tabname']
                                    city_object['field_marker_description'] = cleaned_bhopal_dict['field_marker_description']
                                    city_object['field_video_note'] = cleaned_bhopal_dict['field_video_note']
                                    city_object['field_audio_path'] = cleaned_bhopal_dict['field_audio_path']
                                    city_object['field_document_title'] = cleaned_bhopal_dict['field_document_title']
                                    city_object['field_node_id'] = cleaned_bhopal_dict['field_node_id']
                                    city_object['field_marker_introduction'] = cleaned_bhopal_dict['field_marker_introduction']
                                    city_object['field_pin_position_x'] = cleaned_bhopal_dict['field_pin_position_x']
                                    city_object['field_pin_position_y'] = cleaned_bhopal_dict['field_pin_position_y']
                                    filtered_output.append(city_object)
                        return ({"results": filtered_output}), 200
                    
                    # unable to parse Shahjahanabad
                    if 'Shahjahanabad' in cleaned_data:
                        shahjahanabad_cleaned_data_list = cleaned_data.split('}')
                        for item in shahjahanabad_cleaned_data_list:
                            shahjahanabad_cleaned_item = item.lstrip(',')
                            shahjahanabad_cleaned_item = shahjahanabad_cleaned_item + '}'
                            if len(shahjahanabad_cleaned_item) > 1:
                                shahjahanabad_cleaned_data_dump = json.dumps(shahjahanabad_cleaned_item, indent=2)
                                shahjahanabad_cleaned_data_dict = json.loads(shahjahanabad_cleaned_data_dump)
                                shahjahanabad_cleaned_data_dict = json.loads(shahjahanabad_cleaned_data_dict)
                                # print('debug', shahjahanabad_cleaned_data_dict)
                                for marker_item in marker:
                                    # print(shahjahanabad_cleaned_data_dict['field_pin_type'])
                                    if shahjahanabad_cleaned_data_dict['field_pin_type'] == marker_item:
                                        city_object['nid'] = shahjahanabad_cleaned_data_dict['nid']
                                        city_object['title'] = shahjahanabad_cleaned_data_dict['title']
                                        city_object['field_marker_introduction_image'] = shahjahanabad_cleaned_data_dict['field_marker_introduction_image']
                                        city_object['field_marker_link_text'] = shahjahanabad_cleaned_data_dict['field_marker_link_text']
                                        city_object['field_pin_type'] = shahjahanabad_cleaned_data_dict['field_pin_type']
                                        city_object['field_marker_slide_image'] = shahjahanabad_cleaned_data_dict['field_marker_slide_image']
                                        city_object['field_video_path'] = shahjahanabad_cleaned_data_dict['field_video_path']
                                        city_object['field_tabname'] = shahjahanabad_cleaned_data_dict['field_tabname']
                                        city_object['field_marker_description'] = shahjahanabad_cleaned_data_dict['field_marker_description']
                                        city_object['field_video_note'] = shahjahanabad_cleaned_data_dict['field_video_note']
                                        city_object['field_audio_path'] = shahjahanabad_cleaned_data_dict['field_audio_path']
                                        city_object['field_document_title'] = shahjahanabad_cleaned_data_dict['field_document_title']
                                        city_object['field_node_id'] = shahjahanabad_cleaned_data_dict['field_node_id']
                                        city_object['field_marker_introduction'] = shahjahanabad_cleaned_data_dict['field_marker_introduction']
                                        city_object['field_pin_position_x'] = shahjahanabad_cleaned_data_dict['field_pin_position_x']
                                        city_object['field_pin_position_y'] = shahjahanabad_cleaned_data_dict['field_pin_position_y']
                                        filtered_output.append(city_object)
                                        # print(filtered_output)
                        # print('debug:', filtered_output)
                        return jsonify({"results": filtered_output}),200

                        #             city_object['nid'] = shahjahanabad_cleaned_data_dict['nid']
                        #             city_object['title'] = shahjahanabad_cleaned_data_dict['title']
                        #             city_object['field_marker_introduction_image'] = shahjahanabad_cleaned_data_dict['field_marker_introduction_image']
                        #             city_object['field_marker_link_text'] = shahjahanabad_cleaned_data_dict['field_marker_link_text']
                        #             city_object['field_pin_type'] = shahjahanabad_cleaned_data_dict['field_pin_type']
                        #             city_object['field_marker_slide_image'] = shahjahanabad_cleaned_data_dict['field_marker_slide_image']
                        #             city_object['field_video_path'] = shahjahanabad_cleaned_data_dict['field_video_path']
                        #             city_object['field_tabname'] = shahjahanabad_cleaned_data_dict['field_tabname']
                        #             city_object['field_marker_description'] = shahjahanabad_cleaned_data_dict['field_marker_description']
                        #             city_object['field_video_note'] = shahjahanabad_cleaned_data_dict['field_video_note']
                        #             city_object['field_audio_path'] = shahjahanabad_cleaned_data_dict['field_audio_path']
                        #             city_object['field_document_title'] = shahjahanabad_cleaned_data_dict['field_document_title']
                        #             city_object['field_node_id'] = shahjahanabad_cleaned_data_dict['field_node_id']
                        #             city_object['field_marker_introduction'] = shahjahanabad_cleaned_data_dict['field_marker_introduction']
                        #             city_object['field_pin_position_x'] = shahjahanabad_cleaned_data_dict['field_pin_position_x']
                        #             city_object['field_pin_position_y'] = shahjahanabad_cleaned_data_dict['field_pin_position_y']
                        #             filtered_output.append(city_object)
                        # return ({"results": filtered_output}), 200

                    # generic for the rest
                    if cleaned_data != '':
                        cleaned_data_dict = json.loads(cleaned_data)
                        # print(cleaned_data_dict)
                        for marker_item in marker:
                            if cleaned_data_dict['field_pin_type'] == marker_item:
                                city_object['nid'] = cleaned_data_dict['nid']
                                city_object['title'] = cleaned_data_dict['title']
                                city_object['field_marker_introduction_image'] = cleaned_data_dict['field_marker_introduction_image']
                                city_object['field_marker_link_text'] = cleaned_data_dict['field_marker_link_text']
                                city_object['field_pin_type'] = cleaned_data_dict['field_pin_type']
                                city_object['field_marker_slide_image'] = cleaned_data_dict['field_marker_slide_image']
                                city_object['field_video_path'] = cleaned_data_dict['field_video_path']
                                city_object['field_tabname'] = cleaned_data_dict['field_tabname']
                                city_object['field_marker_description'] = cleaned_data_dict['field_marker_description']
                                city_object['field_video_note'] = cleaned_data_dict['field_video_note']
                                city_object['field_audio_path'] = cleaned_data_dict['field_audio_path']
                                city_object['field_document_title'] = cleaned_data_dict['field_document_title']
                                city_object['field_node_id'] = cleaned_data_dict['field_node_id']
                                city_object['field_marker_introduction'] = cleaned_data_dict['field_marker_introduction']
                                city_object['field_pin_position_x'] = cleaned_data_dict['field_pin_position_x']
                                city_object['field_pin_position_y'] = cleaned_data_dict['field_pin_position_y']
                                filtered_output.append(city_object)
        return ({"results": filtered_output}), 200
    except Exception as e:
        print(e)
        return jsonify({"results": "Could not fetch data from historical data API. Try Again!"}), 400
 

# @app.get('/rest-v1/filtered_historical_cities')
# def historical_city_filter():
#     city = request.args.get('city')
#     marker = request.args.get('marker', 'Built Heritage')
#     print(city, marker)
#     filtered_output = []
#     try:
#         response = requests.get('https://icvtesting.nvli.in/rest-v1/historic-cities', verify=False)
#         if response.status_code == 200:
#             data = json.loads(response.text)['results']

#         for hist_city in data:
#             if hist_city['title'] == city:
#                 hist_city_data_list = hist_city['field_markers'].split(']')

#                 for item in hist_city_data_list:
#                     city_object = {}
#                     cleaned_data = item.replace('[', '')
#                     cleaned_data = cleaned_data.lstrip(',')

#                     if cleaned_data != '':
#                         cleaned_data_dict = json.loads(cleaned_data)

#                         if cleaned_data_dict['field_pin_type'] == marker:
#                             city_object['nid'] = cleaned_data_dict['nid']
#                             city_object['title'] = cleaned_data_dict['title']
#                             city_object['field_marker_introduction_image'] = cleaned_data_dict['field_marker_introduction_image']
#                             city_object['field_marker_link_text'] = cleaned_data_dict['field_marker_link_text']
#                             city_object['field_pin_type'] = cleaned_data_dict['field_pin_type']
#                             city_object['field_marker_slide_image'] = cleaned_data_dict['field_marker_slide_image']
#                             city_object['field_video_path'] = cleaned_data_dict['field_video_path']
#                             city_object['field_tabname'] = cleaned_data_dict['field_tabname']
#                             city_object['field_marker_description'] = cleaned_data_dict['field_marker_description']
#                             city_object['field_video_note'] = cleaned_data_dict['field_video_note']
#                             city_object['field_audio_path'] = cleaned_data_dict['field_audio_path']
#                             city_object['field_document_title'] = cleaned_data_dict['field_document_title']
#                             city_object['field_node_id'] = cleaned_data_dict['field_node_id']
#                             city_object['field_marker_introduction'] = cleaned_data_dict['field_marker_introduction']
#                             city_object['field_pin_position_x'] = cleaned_data_dict['field_pin_position_x']
#                             city_object['field_pin_position_y'] = cleaned_data_dict['field_pin_position_y']
#                             filtered_output.append(city_object)
#         return ({"results": filtered_output}), 200
#     except Exception as e:
#         return jsonify({"results": "Could not fetch data from historical data API. Try Again!"}), 400
 

app.run(debug=True)
 
                            
    
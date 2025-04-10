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
            
            if city != 'Kolkata':
                for hist_city in data:
                    if str(hist_city['title'].lower()) == str(city.strip().lower()):
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:
                            city_object = {}
                            cleaned_data = hist_city_item.replace('[', '')
                            cleaned_data = cleaned_data.lstrip(',')
                            cleaned_data = cleaned_data.replace("'", '"')

                            if cleaned_data != '':
                                cleaned_data_dict = json.loads(cleaned_data)
                                # print(cleaned_data_dict)
                                for marker_item in marker:
                                    # print(cleaned_data_dict['nid'],cleaned_data_dict['title'] )
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
            
            if city == 'Kolkata':
                print('here')
                for hist_city in data:
                    if hist_city['title'].lower() == 'kolkata':
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:

                            cleaned_data = hist_city_item.replace('[', '')

                            len_split_data = (len(cleaned_data.split('},')))
                            if len_split_data > 1:
                                for final_kolkata_data in cleaned_data.split('},'):
                                    final_kolkata_data = final_kolkata_data + '}'
                                    try:
                                        kolkata_city_obj = {}
                                        kolkata_json_parsed_data = json.loads(final_kolkata_data)

                                        for marker_item in marker:
                                            if kolkata_json_parsed_data['field_pin_type'] == marker_item:
                                                kolkata_city_obj['nid'] = kolkata_json_parsed_data['nid']
                                                kolkata_city_obj['title'] = kolkata_json_parsed_data['title']
                                                kolkata_city_obj['field_marker_introduction_image'] = kolkata_json_parsed_data['field_marker_introduction_image']
                                                kolkata_city_obj['field_marker_link_text'] = kolkata_json_parsed_data['field_marker_link_text']
                                                kolkata_city_obj['field_pin_type'] = kolkata_json_parsed_data['field_pin_type']
                                                kolkata_city_obj['field_marker_slide_image'] = kolkata_json_parsed_data['field_marker_slide_image']
                                                kolkata_city_obj['field_video_path'] = kolkata_json_parsed_data['field_video_path']
                                                kolkata_city_obj['field_tabname'] = kolkata_json_parsed_data['field_tabname']
                                                kolkata_city_obj['field_marker_description'] = kolkata_json_parsed_data['field_marker_description']
                                                kolkata_city_obj['field_video_note'] = kolkata_json_parsed_data['field_video_note']
                                                kolkata_city_obj['field_audio_path'] = kolkata_json_parsed_data['field_audio_path']
                                                kolkata_city_obj['field_document_title'] = kolkata_json_parsed_data['field_document_title']
                                                kolkata_city_obj['field_node_id'] = kolkata_json_parsed_data['field_node_id']
                                                kolkata_city_obj['field_marker_introduction'] = kolkata_json_parsed_data['field_marker_introduction']
                                                kolkata_city_obj['field_pin_position_x'] = kolkata_json_parsed_data['field_pin_position_x']
                                                kolkata_city_obj['field_pin_position_y'] = kolkata_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(kolkata_city_obj)
                                    except json.JSONDecodeError as e:
                                            pass
                                    break
                            else:
                                print('here')
                                if cleaned_data != '':
                                    kolkata_city_obj = {}
                                    cleaned_data = cleaned_data.lstrip(',')
                                    try:
                                        kolkata_json_parsed_data = json.loads(cleaned_data)
                                        kolkata_json_parsed_data = json.loads(final_kolkata_data)
                                        for marker_item in marker:
                                            if kolkata_json_parsed_data['field_pin_type'] == marker_item:
                                                kolkata_city_obj['nid'] = kolkata_json_parsed_data['nid']
                                                kolkata_city_obj['title'] = kolkata_json_parsed_data['title']
                                                kolkata_city_obj['field_marker_introduction_image'] = kolkata_json_parsed_data['field_marker_introduction_image']
                                                kolkata_city_obj['field_marker_link_text'] = kolkata_json_parsed_data['field_marker_link_text']
                                                kolkata_city_obj['field_pin_type'] = kolkata_json_parsed_data['field_pin_type']
                                                kolkata_city_obj['field_marker_slide_image'] = kolkata_json_parsed_data['field_marker_slide_image']
                                                kolkata_city_obj['field_video_path'] = kolkata_json_parsed_data['field_video_path']
                                                kolkata_city_obj['field_tabname'] = kolkata_json_parsed_data['field_tabname']
                                                kolkata_city_obj['field_marker_description'] = kolkata_json_parsed_data['field_marker_description']
                                                kolkata_city_obj['field_video_note'] = kolkata_json_parsed_data['field_video_note']
                                                kolkata_city_obj['field_audio_path'] = kolkata_json_parsed_data['field_audio_path']
                                                kolkata_city_obj['field_document_title'] = kolkata_json_parsed_data['field_document_title']
                                                kolkata_city_obj['field_node_id'] = kolkata_json_parsed_data['field_node_id']
                                                kolkata_city_obj['field_marker_introduction'] = kolkata_json_parsed_data['field_marker_introduction']
                                                kolkata_city_obj['field_pin_position_x'] = kolkata_json_parsed_data['field_pin_position_x']
                                                kolkata_city_obj['field_pin_position_y'] = kolkata_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(kolkata_city_obj)
                                    except Exception as e:
                                        pass                   
                return jsonify({"results": filtered_output})            
                               
            if city == 'Bhopal':
                for hist_city in data:
                    if hist_city['title'].lower() == 'bhopal':
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:

                            cleaned_data = hist_city_item.replace('[', '')

                            len_split_data = (len(cleaned_data.split('},')))
                            if len_split_data > 1:
                                for final_bhopal_data in cleaned_data.split('},'):
                                    final_bhopal_data = final_bhopal_data + '}'
                                    try:
                                        bhoapl_city_obj = {}
                                        bhopal_json_parsed_data = json.loads(final_bhopal_data)

                                        for marker_item in marker:
                                            if bhopal_json_parsed_data['field_pin_type'] == marker_item:
                                                bhoapl_city_obj['nid'] = bhopal_json_parsed_data['nid']
                                                bhoapl_city_obj['title'] = bhopal_json_parsed_data['title']
                                                bhoapl_city_obj['field_marker_introduction_image'] = bhopal_json_parsed_data['field_marker_introduction_image']
                                                bhoapl_city_obj['field_marker_link_text'] = bhopal_json_parsed_data['field_marker_link_text']
                                                bhoapl_city_obj['field_pin_type'] = bhopal_json_parsed_data['field_pin_type']
                                                bhoapl_city_obj['field_marker_slide_image'] = bhopal_json_parsed_data['field_marker_slide_image']
                                                bhoapl_city_obj['field_video_path'] = bhopal_json_parsed_data['field_video_path']
                                                bhoapl_city_obj['field_tabname'] = bhopal_json_parsed_data['field_tabname']
                                                bhoapl_city_obj['field_marker_description'] = bhopal_json_parsed_data['field_marker_description']
                                                bhoapl_city_obj['field_video_note'] = bhopal_json_parsed_data['field_video_note']
                                                bhoapl_city_obj['field_audio_path'] = bhopal_json_parsed_data['field_audio_path']
                                                bhoapl_city_obj['field_document_title'] = bhopal_json_parsed_data['field_document_title']
                                                bhoapl_city_obj['field_node_id'] = bhopal_json_parsed_data['field_node_id']
                                                bhoapl_city_obj['field_marker_introduction'] = bhopal_json_parsed_data['field_marker_introduction']
                                                bhoapl_city_obj['field_pin_position_x'] = bhopal_json_parsed_data['field_pin_position_x']
                                                bhoapl_city_obj['field_pin_position_y'] = bhopal_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(bhoapl_city_obj)
                                    except json.JSONDecodeError as e:
                                            pass
                                    break
                            else:
                                if cleaned_data != '':
                                    bhoapl_city_obj = {}
                                    cleaned_data = cleaned_data.lstrip(',')
                                    try:
                                        bhoapl_city_obj = json.loads(cleaned_data)
                                        bhoapl_json_parsed_data = json.loads(bhoapl_city_obj)
                                        for marker_item in marker:
                                            if bhoapl_json_parsed_data['field_pin_type'] == marker_item:
                                                bhoapl_city_obj['nid'] = bhoapl_json_parsed_data['nid']
                                                bhoapl_city_obj['title'] = bhoapl_json_parsed_data['title']
                                                bhoapl_city_obj['field_marker_introduction_image'] = bhoapl_json_parsed_data['field_marker_introduction_image']
                                                bhoapl_city_obj['field_marker_link_text'] = bhoapl_json_parsed_data['field_marker_link_text']
                                                bhoapl_city_obj['field_pin_type'] = bhoapl_json_parsed_data['field_pin_type']
                                                bhoapl_city_obj['field_marker_slide_image'] = bhoapl_json_parsed_data['field_marker_slide_image']
                                                bhoapl_city_obj['field_video_path'] = bhoapl_json_parsed_data['field_video_path']
                                                bhoapl_city_obj['field_tabname'] = bhoapl_json_parsed_data['field_tabname']
                                                bhoapl_city_obj['field_marker_description'] = bhoapl_json_parsed_data['field_marker_description']
                                                bhoapl_city_obj['field_video_note'] = bhoapl_json_parsed_data['field_video_note']
                                                bhoapl_city_obj['field_audio_path'] = bhoapl_json_parsed_data['field_audio_path']
                                                bhoapl_city_obj['field_document_title'] = bhoapl_json_parsed_data['field_document_title']
                                                bhoapl_city_obj['field_node_id'] = bhoapl_json_parsed_data['field_node_id']
                                                bhoapl_city_obj['field_marker_introduction'] = bhoapl_json_parsed_data['field_marker_introduction']
                                                bhoapl_city_obj['field_pin_position_x'] = bhoapl_json_parsed_data['field_pin_position_x']
                                                bhoapl_city_obj['field_pin_position_y'] = bhoapl_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(bhoapl_city_obj)
                                    except Exception as e:
                                        pass                   
                return jsonify({"results": filtered_output})       

            if city == 'Shahjahanabad':
                for hist_city in data:
                    if hist_city['title'].lower() == 'shahjahanabad':
                        hist_city_data_list = hist_city['field_markers'].split(']')
                        for hist_city_item in hist_city_data_list:

                            cleaned_data = hist_city_item.replace('[', '')

                            len_split_data = (len(cleaned_data.split('},')))
                            if len_split_data > 1:
                                for final_bhopal_data in cleaned_data.split('},'):
                                    final_bhopal_data = final_bhopal_data + '}'
                                    try:
                                        shahjahanabad_city_obj = {}
                                        shahjahanabad_json_parsed_data = json.loads(final_bhopal_data)

                                        for marker_item in marker:
                                            if shahjahanabad_json_parsed_data['field_pin_type'] == marker_item:
                                                shahjahanabad_city_obj['nid'] = shahjahanabad_json_parsed_data['nid']
                                                shahjahanabad_city_obj['title'] = shahjahanabad_json_parsed_data['title']
                                                shahjahanabad_city_obj['field_marker_introduction_image'] = shahjahanabad_json_parsed_data['field_marker_introduction_image']
                                                shahjahanabad_city_obj['field_marker_link_text'] = shahjahanabad_json_parsed_data['field_marker_link_text']
                                                shahjahanabad_city_obj['field_pin_type'] = shahjahanabad_json_parsed_data['field_pin_type']
                                                shahjahanabad_city_obj['field_marker_slide_image'] = shahjahanabad_json_parsed_data['field_marker_slide_image']
                                                shahjahanabad_city_obj['field_video_path'] = shahjahanabad_json_parsed_data['field_video_path']
                                                shahjahanabad_city_obj['field_tabname'] = shahjahanabad_json_parsed_data['field_tabname']
                                                shahjahanabad_city_obj['field_marker_description'] = shahjahanabad_json_parsed_data['field_marker_description']
                                                shahjahanabad_city_obj['field_video_note'] = shahjahanabad_json_parsed_data['field_video_note']
                                                shahjahanabad_city_obj['field_audio_path'] = shahjahanabad_json_parsed_data['field_audio_path']
                                                shahjahanabad_city_obj['field_document_title'] = shahjahanabad_json_parsed_data['field_document_title']
                                                shahjahanabad_city_obj['field_node_id'] = shahjahanabad_json_parsed_data['field_node_id']
                                                shahjahanabad_city_obj['field_marker_introduction'] = shahjahanabad_json_parsed_data['field_marker_introduction']
                                                shahjahanabad_city_obj['field_pin_position_x'] = shahjahanabad_json_parsed_data['field_pin_position_x']
                                                shahjahanabad_city_obj['field_pin_position_y'] = shahjahanabad_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(shahjahanabad_city_obj)
                                    except json.JSONDecodeError as e:
                                            pass
                                    break
                            else:
                                if cleaned_data != '':
                                    bhoapl_city_obj = {}
                                    cleaned_data = cleaned_data.lstrip(',')
                                    try:
                                        shahjahanabad_city_obj = json.loads(cleaned_data)
                                        shahjahanabad_json_parsed_data = json.loads(shahjahanabad_city_obj)
                                        for marker_item in marker:
                                            if bhoapl_json_parsed_data['field_pin_type'] == marker_item:
                                                shahjahanabad_city_obj['nid'] = shahjahanabad_json_parsed_data['nid']
                                                shahjahanabad_city_obj['title'] = shahjahanabad_json_parsed_data['title']
                                                shahjahanabad_city_obj['field_marker_introduction_image'] = shahjahanabad_json_parsed_data['field_marker_introduction_image']
                                                shahjahanabad_city_obj['field_marker_link_text'] = shahjahanabad_json_parsed_data['field_marker_link_text']
                                                shahjahanabad_city_obj['field_pin_type'] = shahjahanabad_json_parsed_data['field_pin_type']
                                                shahjahanabad_city_obj['field_marker_slide_image'] = shahjahanabad_json_parsed_data['field_marker_slide_image']
                                                shahjahanabad_city_obj['field_video_path'] = shahjahanabad_json_parsed_data['field_video_path']
                                                shahjahanabad_city_obj['field_tabname'] = shahjahanabad_json_parsed_data['field_tabname']
                                                shahjahanabad_city_obj['field_marker_description'] = shahjahanabad_json_parsed_data['field_marker_description']
                                                shahjahanabad_city_obj['field_video_note'] = shahjahanabad_json_parsed_data['field_video_note']
                                                shahjahanabad_city_obj['field_audio_path'] = shahjahanabad_json_parsed_data['field_audio_path']
                                                shahjahanabad_city_obj['field_document_title'] = shahjahanabad_json_parsed_data['field_document_title']
                                                shahjahanabad_city_obj['field_node_id'] = shahjahanabad_json_parsed_data['field_node_id']
                                                shahjahanabad_city_obj['field_marker_introduction'] = shahjahanabad_json_parsed_data['field_marker_introduction']
                                                shahjahanabad_city_obj['field_pin_position_x'] = shahjahanabad_json_parsed_data['field_pin_position_x']
                                                shahjahanabad_city_obj['field_pin_position_y'] = shahjahanabad_json_parsed_data['field_pin_position_y']
                                                filtered_output.append(shahjahanabad_city_obj)
                                    except Exception as e:
                                        pass                   
                return jsonify({"results": filtered_output})            
                         
                    
        except Exception as e:
            print(e)



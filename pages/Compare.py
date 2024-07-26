import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title='LCA',page_icon='bar_chart')
st.title('Compare (Scenario Planning)')
glass=pd.read_excel('Data/GLASS.xlsx')
plastic=pd.read_excel('Data/Plastics.xlsx')
metal=pd.read_excel('Data/Metal.xlsx')
material_type=['Plastic','Metal']
pcr_factors=pd.read_excel('Data/PCR_FACTORS.xlsx')
pcr_factors=pcr_factors.fillna(0)
metal_processing=pd.read_excel('Data/Metal Processing.xlsx')
plastic_processing=pd.read_excel('Data/Plastic Processing.xlsx')
transport=pd.read_excel('Data/Transport.xlsx')
eol=pd.read_excel('Data/End Of Life.xlsx')
eol=eol.fillna(0)
eol_data=pd.read_excel('Data/End Of Life Data.xlsx')

def raw_material_user_input_1():
    metal_weight=0
    plastic_weight=0
    glass_weight=0
    st.title('Raw Material')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _component_name=st.text_input("Component Name")
    with col2:
        _component_weight=st.number_input("Weight",value=100)
    with col3:
        _component_type=st.selectbox("Material Type",material_type)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        if _component_type=='Plastic':
            plastic_weight=plastic_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component",plastic,index=10)
            _component_ef=plastic.loc[plastic['Impact category'] == str(_component_specific_type)].values[0][1]
        elif _component_type=='Glass':
            glass_weight=glass_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component",glass,index=10)
            _component_ef=glass.loc[glass['Impact category'] == _component_specific_type].values[0][1]
        else:
            metal_weight=metal_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component",metal,index=10)
            _component_ef=metal.loc[metal['Impact category'] == _component_specific_type].values[0][1]
    with col5:
        _component_recycle=st.selectbox("Recycle",['Yes','No'])
    with col6:
        _component_pcr_factor=st.selectbox("PCR",['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
    col9,col10,col11,col12=st.columns(4)
    with col7:
        if _component_type=='Plastic':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",plastic_processing,index=0)
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        elif _component_type=='Glass':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",[])
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        if _component_type=='Metal':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",metal_processing,index=0)
            _component_production_ef=metal_processing.loc[metal_processing['Impact category'] == _component_manufaturing_process].values[0][1]
    with col8:
        _wastage=st.number_input("Waste Percent",value=10)
    _weight_including_waste=(_wastage+1)*_component_weight
    _component_material_footprint=(_weight_including_waste*_component_ef*int(_component_pcr_factor[0:2]))/100000
    _component_production_footprint=(_weight_including_waste*_component_production_ef)/1000
    _recycle_factor=(pcr_factors.loc[pcr_factors['Component']==_component_specific_type].values[0][1]/1000)*(int(_component_pcr_factor[0:2])*_weight_including_waste/100)
    _total_footprint=float(_component_material_footprint)+_component_production_footprint+(_recycle_factor)
    input_data={'component_name':_component_name,
                'component_weight':_component_weight,
                'component_type':_component_type,
                'component_specific_type':_component_specific_type,
                'component_recycle':_component_recycle,
                'component_pcr_factor':_component_pcr_factor,
                'component_manufaturing_process':_component_manufaturing_process,
                'wastage':_wastage}
    prediction={'weight_including_waste':_weight_including_waste,'component_material_footprint':_component_material_footprint,'component_production_footprint':_component_production_footprint,'recycle_facto':_recycle_factor,'total_footprint':_total_footprint}
    input_dataframe=pd.DataFrame(input_data,index=[0])
    prediction_dataframe=pd.DataFrame(prediction,index=[0])

    #st.table(input_dataframe)
    
    return (input_data,plastic_weight,glass_weight,metal_weight,_component_material_footprint+_recycle_factor,_component_production_footprint)
def incoming_transport_input_1():
    st.title('Incoming Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Incoming Description")
    with col2:
        _incoming_transport_weight=st.number_input("Incoming Transport Weight",value=100)
    with col3:
        _transport_type=st.selectbox("Material Type",transport['Impact category'].values,index=0)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Incoming Frieght Distance",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    incoming_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(incoming_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (incoming_transport_input_data,_transport_footprint)
def distribution_transport_input_1():
    st.title('Distribution Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Distribution Description")
    with col2:
        _incoming_transport_weight=st.number_input("Distribution Transport Weight",value=100)
    with col3:
        _transport_type=st.selectbox("Transport Type",transport['Impact category'].values,index=1)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Distribution Frieght Distance",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    distribution_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(distribution_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (distribution_transport_input_data,_transport_footprint)
def eol_caluclation_1(plastic_,glass_,metal_,input_data):
    st.title('End OF Life')
    eol_lf={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to sanitary landfill/CH S','Glass':0}
    eol_efw={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to municipal incineration/CH S','Glass':0}
    _type_of_recycle=st.selectbox(" Type of Recycle",['Unrecyclable','Noraml Recycling','Milk and Detergents'])
    if _type_of_recycle=='Unrecyclable':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][1]
        
    elif  _type_of_recycle=='Noraml Recycling':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][2]
        
    else:
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][3]
    

    eol_lf_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    eol_efw_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    final_eol_value=eol_lf_value+eol_efw_value
    return(final_eol_value)


def raw_material_user_input_2():
    metal_weight=0
    plastic_weight=0
    glass_weight=0
    st.title('Raw Material')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _component_name=st.text_input("Component Name 2")
    with col2:
        _component_weight=st.number_input("Weight 2",value=100)
    with col3:
        _component_type=st.selectbox("Material Type 2",material_type)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        if _component_type=='Plastic':
            plastic_weight=plastic_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 2",plastic,index=3)
            _component_ef=plastic.loc[plastic['Impact category'] == str(_component_specific_type)].values[0][1]
        elif _component_type=='Glass':
            glass_weight=glass_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 2",glass)
            _component_ef=glass.loc[glass['Impact category'] == _component_specific_type].values[0][1]
        else:
            metal_weight=metal_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 2",metal)
            _component_ef=metal.loc[metal['Impact category'] == _component_specific_type].values[0][1]
    with col5:
        _component_recycle=st.selectbox("Recycle 2",['Yes','No'])
    with col6:
        _component_pcr_factor=st.selectbox("PCR 2",['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
    col9,col10,col11,col12=st.columns(4)
    with col7:
        if _component_type=='Plastic':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 2",plastic_processing,index=2)
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        elif _component_type=='Glass':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 2",[])
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        if _component_type=='Metal':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 2",metal_processing)
            _component_production_ef=metal_processing.loc[metal_processing['Impact category'] == _component_manufaturing_process].values[0][1]
    with col8:
        _wastage=st.number_input("Waste Percent 2",value=10)
    _weight_including_waste=(_wastage+1)*_component_weight
    _component_material_footprint=(_weight_including_waste*_component_ef*int(_component_pcr_factor[0:2]))/100000
    _component_production_footprint=(_weight_including_waste*_component_production_ef)/1000
    _recycle_factor=(pcr_factors.loc[pcr_factors['Component']==_component_specific_type].values[0][1]/1000)*(int(_component_pcr_factor[0:2])*_weight_including_waste/100)

    _total_footprint=float(_component_material_footprint)+_component_production_footprint+(_recycle_factor)
    input_data={'component_name':_component_name,
                'component_weight':_component_weight,
                'component_type':_component_type,
                'component_specific_type':_component_specific_type,
                'component_recycle':_component_recycle,
                'component_pcr_factor':_component_pcr_factor,
                'component_manufaturing_process':_component_manufaturing_process,
                'wastage':_wastage}
    prediction={'weight_including_waste':_weight_including_waste,'component_material_footprint':_component_material_footprint,'component_production_footprint':_component_production_footprint,'recycle_facto':_recycle_factor,'total_footprint':_total_footprint}
    input_dataframe=pd.DataFrame(input_data,index=[0])
    prediction_dataframe=pd.DataFrame(prediction,index=[0])

    #st.table(input_dataframe)
    
    return (input_data,plastic_weight,glass_weight,metal_weight,_component_material_footprint+_recycle_factor,_component_production_footprint)
def incoming_transport_input_2():
    st.title('Incoming Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Incoming Description 2")
    with col2:
        _incoming_transport_weight=st.number_input("Incoming Transport Weight 2",value=100)
    with col3:
        _transport_type=st.selectbox("Material Type 2",transport['Impact category'].values,index=3)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Incoming Frieght Distance 2",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    incoming_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(incoming_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (incoming_transport_input_data,_transport_footprint)
def distribution_transport_input_2():
    st.title('Distribution Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Distribution Description 2")
    with col2:
        _incoming_transport_weight=st.number_input("Distribution Transport Weight 2",value=100)
    with col3:
        _transport_type=st.selectbox("Transport Type 2",transport['Impact category'].values,index=3)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Distribution Frieght Distance 2",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    distribution_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(distribution_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (distribution_transport_input_data,_transport_footprint)
def eol_caluclation_2(plastic_,glass_,metal_,input_data):
    st.title('End OF Life')
    eol_lf={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to sanitary landfill/CH S','Glass':0}
    eol_efw={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to municipal incineration/CH S','Glass':0}
    _type_of_recycle=st.selectbox("Type of Recycle",['Unrecyclable','Noraml Recycling','Milk and Detergents'])
    if _type_of_recycle=='Unrecyclable':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][1]
        
    elif  _type_of_recycle=='Noraml Recycling':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][2]
        
    else:
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][3]
    

    eol_lf_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    eol_efw_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    final_eol_value=eol_lf_value+eol_efw_value
    return(final_eol_value)

def raw_material_user_input_3():
    metal_weight=0
    plastic_weight=0
    glass_weight=0
    st.title('Raw Material')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _component_name=st.text_input("Component Name 3")
    with col2:
        _component_weight=st.number_input("Weight 3",value=100)
    with col3:
        _component_type=st.selectbox("Material Type 3",material_type)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        if _component_type=='Plastic':
            plastic_weight=plastic_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 3",plastic,index=12)
            _component_ef=plastic.loc[plastic['Impact category'] == str(_component_specific_type)].values[0][1]
        elif _component_type=='Glass':
            glass_weight=glass_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 3",glass)
            _component_ef=glass.loc[glass['Impact category'] == _component_specific_type].values[0][1]
        else:
            metal_weight=metal_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component 3",metal)
            _component_ef=metal.loc[metal['Impact category'] == _component_specific_type].values[0][1]
    with col5:
        _component_recycle=st.selectbox("Recycle 3",['Yes','No'])
    with col6:
        _component_pcr_factor=st.selectbox("PCR 3",['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
    col9,col10,col11,col12=st.columns(4)
    with col7:
        if _component_type=='Plastic':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 3",plastic_processing,index=3)
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        elif _component_type=='Glass':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 3",[])
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        if _component_type=='Metal':
            _component_manufaturing_process=st.selectbox("Manufacturing Process 3",metal_processing)
            _component_production_ef=metal_processing.loc[metal_processing['Impact category'] == _component_manufaturing_process].values[0][1]
    with col8: 
        _wastage=st.number_input("Waste Percent 3",value=10)
        _weight_including_waste=(_wastage+1)*_component_weight
        _component_material_footprint=(_weight_including_waste*_component_ef*int(_component_pcr_factor[0:2]))/100000
        _component_production_footprint=(_weight_including_waste*_component_production_ef)/1000
        _recycle_factor=(pcr_factors.loc[pcr_factors['Component']==_component_specific_type].values[0][1]/1000)*(int(_component_pcr_factor[0:2])*_weight_including_waste/100)
        
        _total_footprint=float(_component_material_footprint)+_component_production_footprint+(_recycle_factor)
        input_data={'component_name':_component_name,
                    'component_weight':_component_weight,
                    'component_type':_component_type,
                    'component_specific_type':_component_specific_type,
                    'component_recycle':_component_recycle,
                    'component_pcr_factor':_component_pcr_factor,
                    'component_manufaturing_process':_component_manufaturing_process,
                    'wastage':_wastage}
        prediction={'weight_including_waste':_weight_including_waste,'component_material_footprint':_component_material_footprint,'component_production_footprint':_component_production_footprint,'recycle_facto':_recycle_factor,'total_footprint':_total_footprint}
        input_dataframe=pd.DataFrame(input_data,index=[0])
        prediction_dataframe=pd.DataFrame(prediction,index=[0])
    
        #st.table(input_dataframe)
    
        return (input_data,plastic_weight,glass_weight,metal_weight,_component_material_footprint+_recycle_factor,_component_production_footprint)
def incoming_transport_input_3():
    st.title('Incoming Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Incoming Description 3")
    with col2:
        _incoming_transport_weight=st.number_input("Incoming Transport Weight 3",value=100)
    with col3:
        _transport_type=st.selectbox("Material Type 3",transport['Impact category'].values,index=5)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Incoming Frieght Distance 3",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    incoming_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(incoming_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (incoming_transport_input_data,_transport_footprint)
def distribution_transport_input_3():
    st.title('Distribution Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Distribution Description 3")
    with col2:
        _incoming_transport_weight=st.number_input("Distribution Transport Weight 3",value=100)
    with col3:
        _transport_type=st.selectbox("Transport Type 3",transport['Impact category'].values,index=5)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Distribution Frieght Distance 3",value=100)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    distribution_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(distribution_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (distribution_transport_input_data,_transport_footprint)
def eol_caluclation_3(plastic_,glass_,metal_,input_data):
    st.title('End OF Life')
    eol_lf={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to sanitary landfill/CH S','Glass':0}
    eol_efw={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to municipal incineration/CH S','Glass':0}
    _type_of_recycle=st.selectbox("Type of Recycle",['Unrecyclable','Noraml Recycling','Milk and Detergents '])
    if _type_of_recycle=='Unrecyclable':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][1]
        
    elif  _type_of_recycle=='Noraml Recycling':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][2]
        
    else:
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][3]
    

    eol_lf_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    eol_efw_value=(eol_data.loc[eol_data['Impact category']==eol_lf['Plastic']].values[0][1])*_carbon*plastic_
    final_eol_value=eol_lf_value+eol_efw_value
    return(final_eol_value)

    

with st.expander("Input 1"):
    raw_material_user_input1,plastic_weight1,glass_weight1,metal_weight1,material1,manufacturing1=raw_material_user_input_1()
    incoming_transport_input1,incoming_transport_footprint1=incoming_transport_input_1()
    distribution_transport_input1,distribution_transport_footprint1=distribution_transport_input_1()
    eol_1=eol_caluclation_1(plastic_weight1,glass_weight1,metal_weight1,raw_material_user_input1)
    Material1=float(material1)*1000

    Manufacturing1=float(manufacturing1)*1000
    Transport1=(incoming_transport_footprint1+distribution_transport_footprint1)*1000
    Total1=Material1+Manufacturing1+Transport1
    graph_data_1={'Category':['Material','Manufacturing','Transport','End Of Life'],'CO2 Equivalent in Kg':[Material1,Manufacturing1,Transport1,eol_1]}
    graph_data_1=pd.DataFrame(graph_data_1)

with st.expander("Input 2"):
    raw_material_user_input2,plastic_weight2,glass_weight2,metal_weight2,material2,manufacturing2=raw_material_user_input_2()
    incoming_transport_input2,incoming_transport_footprint2=incoming_transport_input_2()
    distribution_transport_input2,distribution_transport_footprint2=distribution_transport_input_2()
    eol_2=eol_caluclation_2(plastic_weight2,glass_weight2,metal_weight2,raw_material_user_input2)
    Material2=float(material2)*1000

    Manufacturing2=float(manufacturing2)*1000
    Transport2=(incoming_transport_footprint2+distribution_transport_footprint2)*1000
    Total2=Material2+Manufacturing2+Transport2
    graph_data_2={'Category':['Material','Manufacturing','Transport','End Of Life'],'CO2 Equivalent in Kg':[Material2,Manufacturing2,Transport2,eol_2]}
    graph_data_2=pd.DataFrame(graph_data_2)
with st.expander("Input 3"):
    raw_material_user_input3,plastic_weight3,glass_weight3,metal_weight3,material3,manufacturing3=raw_material_user_input_3()
    incoming_transport_input3,incoming_transport_footprint3=incoming_transport_input_3()
    distribution_transport_input3,distribution_transport_footprint3=distribution_transport_input_3()
    eol_3=eol_caluclation_3(plastic_weight3,glass_weight3,metal_weight3,raw_material_user_input3)
    Material3=float(material3)*1000

    Manufacturing3=float(manufacturing3)*1000
    Transport3=(incoming_transport_footprint3+distribution_transport_footprint3)*1000
    Total3=Material3+Manufacturing3+Transport3
    graph_data_3={'Category':['Material','Manufacturing','Transport','End Of Life'],'CO2 Equivalent in Kg':[Material3,Manufacturing3,Transport3,eol_3]}
    graph_data_3=pd.DataFrame(graph_data_3)
col30,col31,col32=st.columns(3)
with col30:
    st.header("Scenario 1")
    
    fig=px.bar(graph_data_1,x='Category', y='CO2 Equivalent in Kg',color='Category', title='CO2 Emission by Category')
    fig.update_layout(width=400)
    st.plotly_chart(fig)
with col31:
    st.header("Scenario 2")
    

    fig=px.bar(graph_data_2,x='Category', y='CO2 Equivalent in Kg', color='Category', title='CO2 Emission by Category')
    fig.update_layout(width=400)
    st.plotly_chart(fig)
with col32:
    st.header("Scenario 3")
    
    fig=px.histogram(graph_data_3,x='Category', y='CO2 Equivalent in Kg',color='Category', title='CO2 Emission by Category')
    fig.update_layout(width=400)
    st.plotly_chart(fig)
overall_data={"Input Type":['Scenario 1','Scenario 2','Scenario 3'],
              'Specific Component':[raw_material_user_input1['component_specific_type'],raw_material_user_input2['component_specific_type'],raw_material_user_input3['component_specific_type']],
              'Processing Process':[raw_material_user_input1['component_manufaturing_process'],raw_material_user_input2['component_manufaturing_process'],raw_material_user_input3['component_manufaturing_process']],
              'Transport Type':[incoming_transport_input1['transport_type']+ ' & ' +distribution_transport_input1['transport_type'],incoming_transport_input2['transport_type']+ ' & ' +distribution_transport_input2['transport_type'],incoming_transport_input3['transport_type']+ ' & ' +distribution_transport_input3['transport_type']],
              'Material':[Material1,Material2,Material3],
              'Manufacturing':[Manufacturing1,Manufacturing2,Manufacturing3],
              'Transport':[Transport1,Transport2,Transport3],
              'Total':[Total1,Total2,Total3]
              }
st.write(pd.DataFrame(overall_data))

fig1=px.bar(overall_data,x='Specific Component',y=['Material'],color='Input Type',barmode='stack',title='Material Analysis')
fig1.update_layout(yaxis_title='CO2 Equivalent in Kg')
st.plotly_chart(fig1)

fig2=px.bar(overall_data,x='Input Type',y=['Manufacturing'],color='Processing Process',barmode='stack',title='Manufatruing Analysis')
fig2.update_layout(yaxis_title='CO2 Equivalent in Kg')
st.plotly_chart(fig2)
fig3=px.bar(overall_data,x='Input Type',y=['Transport'],color='Transport Type',barmode='stack',title='Transport Analysis')
st.plotly_chart(fig3)

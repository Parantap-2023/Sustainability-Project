import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title='LCA',page_icon='bar_chart')
col50,col51=st.columns([1,2])
with col50:
    st.image('LCA SYMBOL IMAGE.png')
with col51:    
    st.title('LIFE CYCLE ANALYSIS')
glass=pd.read_excel('Data/GLASS.xlsx')
plastic=pd.read_excel('Plastics.xlsx')
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

def raw_material_user_input():
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
            _component_specific_type=st.selectbox("Specific Component",plastic)
            _component_ef=plastic.loc[plastic['Impact category'] == str(_component_specific_type)].values[0][1]
        elif _component_type=='Glass':
            glass_weight=glass_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component",glass)
            _component_ef=glass.loc[glass['Impact category'] == _component_specific_type].values[0][1]
        else:
            metal_weight=metal_weight+_component_weight
            _component_specific_type=st.selectbox("Specific Component",metal)
            _component_ef=metal.loc[metal['Impact category'] == _component_specific_type].values[0][1]
    with col5:
        _component_recycle=st.selectbox("Recycle",['Yes','No'])
    with col6:
        _component_pcr_factor=st.selectbox("PCR",['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
    col9,col10,col11,col12=st.columns(4)
    with col7:
        if _component_type=='Plastic':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",plastic_processing)
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        elif _component_type=='Glass':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",[])
            _component_production_ef=plastic_processing.loc[plastic_processing['Impact category'] == _component_manufaturing_process].values[0][1]
        if _component_type=='Metal':
            _component_manufaturing_process=st.selectbox("Manufacturing Process",metal_processing)
            _component_production_ef=metal_processing.loc[metal_processing['Impact category'] == _component_manufaturing_process].values[0][1]
    with col8:
        _wastage=st.number_input("Waste Percent",value=10)
    _weight_including_waste=(_wastage+1)*_component_weight
    _component_material_footprint=(_weight_including_waste*_component_ef)/10000
    _component_production_footprint=(_weight_including_waste*_component_production_ef)/10000
    _recycle_factor=pcr_factors.loc[pcr_factors['Component']==_component_specific_type].values[0][1]
    _total_footprint=float(_component_material_footprint)+_component_production_footprint-(_recycle_factor)
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
    
    return (input_data,plastic,glass,metal,_component_material_footprint-_recycle_factor,_component_production_footprint)
def incoming_transport_input():
    st.title('Incoming Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Incoming Description")
    with col2:
        _incoming_transport_weight=st.number_input("Incoming Transport Weight",value=100)
    with col3:
        _transport_type=st.selectbox("Material Type",transport['Impact category'].values)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Incoming Frieght Distance",value=1000)
    
    _transport_ef=transport.loc[transport['Impact category']==_transport_type].values[0][1]
    print(_transport_ef)
   
    _transport_footprint=float(_transport_ef)*_incoming_transport_weight*(_distance/1000000)
    print(_transport_footprint)
    incoming_transport_input_data={'description':_description,
                'incoming_transport_weight':_incoming_transport_weight,
                'transport_type':_transport_type,
                'distance':_distance,
                }
    
    input_dataframe=pd.DataFrame(incoming_transport_input_data,index=[0])
    
    
    #st.table(input_dataframe)
    return (incoming_transport_input_data,_transport_footprint)
def distribution_transport_input():
    st.title('Distribution Transport')
    col1,col2,col3,col4=st.columns(4)
    with col1:

        _description=st.text_input("Distribution Description")
    with col2:
        _incoming_transport_weight=st.number_input("Distribution Transport Weight",value=100)
    with col3:
        _transport_type=st.selectbox("Transport Type",transport['Impact category'].values)
    col5,col6,col7,col8=st.columns(4)
    with col4:
        _distance=st.number_input("Distribution Frieght Distance",value=1000)
    
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
def eol_caluclation(plastic,glass,metal,input_data):
    st.title('End OF Life')
    _type_of_recycle=st.selectbox("Type of Recycle",['Unrecyclable','Noraml Recycling','Milk and Detergents'])
    if _type_of_recycle=='Unrecyclable':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][1]
    elif  _type_of_recycle=='NoramlRecycling':
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][2]
    else:
        _carbon=eol.loc[eol['Type of plastic']==input_data['component_specific_type']].values[0][3]
    eol_lf={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to sanitary landfill/CH S','Glass':0}
    eol_efw={'Metal':0,'Plastic':'Disposal, plastics, mixture, 15.3% water, to municipal incineration/CH S','Glass':0}

raw_material_user_input_,plastic_weight,glass_weight,metal_weight,material,manufacturing=raw_material_user_input()
incoming_transport_input_,incoming_transport_footprint=incoming_transport_input()
distribution_transport_input_,distribution_transport_footprint=distribution_transport_input()
eol=eol_caluclation(plastic_weight,glass_weight,metal_weight,raw_material_user_input_)
Material=float(material)*1000

Manufacturing=float(manufacturing)*1000
Transport=(incoming_transport_footprint+distribution_transport_footprint)*1000
graph_data={'Category':['Material','Manufacturing','Transport'],'CO2 Equivalent in Kg':[Material,Manufacturing,Transport]}
graph_data=pd.DataFrame(graph_data)

st.header('Overall Analysis')
col30,col31=st.columns(2)
with col30:
    fig=px.bar(graph_data,x='Category', y='CO2 Equivalent in Kg',color='Category', title='CO2 Emission by Category')
    st.plotly_chart(fig)
with col31:
    fig=px.pie(graph_data,names='Category',values='CO2 Equivalent in Kg',hole=0.5,title='CO2 Emission by Category')
    st.plotly_chart(fig)

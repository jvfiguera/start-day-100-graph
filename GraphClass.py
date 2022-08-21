import plotly.express as px
import matplotlib.pyplot as plt
#, mpld3
import numpy as np

# Constants & Variables

graphs_toshow_list =[]
graph_path ='./static/graphs/'

# Class
class Graphs():
    def __init__(self):
        self.fig_pie    =''
        self.fig_line   =''
        self.fig_choropleth =''
        self.font_size1  =11
        self.font_size2 = 11
        self.graph_dict ={}

    def mth_graph_donuts(self,pLabels,pValues,pNames,pHole,pWidth,pHeight,pTitle,pFilename):
         self.fig_pie = px.pie(labels    =pLabels    #df_failures_bycountry['Failure_Count'].index
                              ,values    =pValues    #df_failures_bycountry.Failure_Count
                              ,names     =pNames     #df_failures_bycountry['Country']
                              ,hole      =pHole      #0.6
                              ,width     =pWidth -50      #400
                              ,height    =pHeight -50    #400
                              )

         self.fig_pie.update_layout(
            autosize            =True,
            font_family         ="Courier New",
            font_color          ="blue",
            font_size           =self.font_size2,
            title_font_family   ="Arial",
            title_font_color    ="blue",
            legend_title_font_color="green",
            title={
                'text':pTitle,
                'y': 1,  # new
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'  # new
            },
            xaxis=dict(rangeslider=dict(visible=False),
                       type="linear")
        )
         self.fig_pie.update_xaxes(title_font_family="Arial", automargin='left+top')
         self.fig_pie.update_traces(textposition='outside', textinfo='percent+label')

         self.fig_pie.write_html(f'{graph_path}{pFilename}')
         self.graph_dict = {'graphname' :f'{graph_path}{pFilename}', 'dimention' : (pWidth, pHeight) }
         graphs_toshow_list.append(self.graph_dict)

    def mth_graph_compare_two_variables(self,pDf_data01,pDf_data02 ,pFilename,pWidth, pHeight):
        fig = plt.figure(figsize=(13, 6), dpi=70)
        ax1 = plt.gca()  # get current axes
        ax2 = ax1.twinx()
        ax1.set_ylim(0, pDf_data01.values.max() + 15)
        ax2.set_ylim(0, pDf_data02.values.max() + 15)
        plt.xticks(fontsize=self.font_size1, rotation=45)
        plt.title("Number of Success and Failures Launches per Year", fontsize=self.font_size1, color='b')
        ax1.set_xlabel("Year", fontsize=self.font_size1, color ='b')
        ax1.set_ylabel("Launches Success", fontsize=self.font_size1, color="g")
        ax2.set_ylabel("Launches Failures", fontsize=self.font_size1, color="r")

        ax1.plot(pDf_data01.index, pDf_data01.values, color='g', linestyle='dashed', markersize=12)
        ax2.plot(pDf_data02.index, pDf_data02.values, color="r", marker='o', markersize=4)
        plt.savefig(f'{graph_path}{pFilename}')
        self.graph_dict = {'graphname': f'{graph_path}{pFilename}', 'dimention': (pWidth, pHeight)}
        graphs_toshow_list.append(self.graph_dict)

        #mpld3.save_html(fig,fileobj=pFilename)
        #graphs_toshow_list.append(f'{graph_path}{pFilename}')

    def mth_graph_sunburst(self,pDf_sunburst,pFilename,pWidth,pHeight,pPath,pValues,pHover_data):
        fig_sunburst = px.sunburst(pDf_sunburst,
                          path  =pPath,
                          values=pValues,
                          color =pValues, hover_data=pHover_data,
                          color_continuous_scale='RdBu',
                          color_continuous_midpoint=np.average(pDf_sunburst[pValues],
                                                               weights=pDf_sunburst[pValues]),
                          width  = pWidth - 50,
                          height = pHeight - 50)

        fig_sunburst.write_html(f'{graph_path}{pFilename}')
        self.graph_dict = {'graphname': f'{graph_path}{pFilename}', 'dimention': (pWidth, pHeight)}
        graphs_toshow_list.append(self.graph_dict)

    def mth_graph_line(self,pDf_data,pX_collumn,pY_collumn,pWidth,pHeight,pFilename,pTitle,pColor):
        if pColor :
            self.fig_line = px.line(pDf_data
                                  ,x        =pDf_data[pX_collumn]
                                  ,y        =pDf_data[pY_collumn]
                                  ,width    =pWidth - 50
                                  ,height   =pHeight -50
                                  ,color    =pColor
                                  ,symbol   =pColor
                                  ,labels = dict(x="Fruit", y="Amount", color="Place")
                                  )
        else :
            self.fig_line = px.line(pDf_data
                                    , x=pDf_data[pX_collumn]
                                    , y=pDf_data[pY_collumn]
                                    , width=pWidth - 50
                                    , height=pHeight - 50
                                    #, labels = dict(x="Fruit", y="Amount", color="Place")
                                    )

        self.fig_line.update_layout(
                autosize                =True,
                font_family             ="Arial",
                font_color              ="blue",
                font_size               =self.font_size2,
                title_font_family       ="Arial",
                title_font_color        ="blue",
                legend_title_font_color ="green",
                title={
                    'text': pTitle,
                    'y': 0.94,  # new
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'  # new
                },
                xaxis=dict(rangeslider=dict(visible=False),
                           type="linear")
        )
        self.fig_line.update_xaxes(title_font_family="Arial", automargin='left+top')
        self.fig_line.update_traces(textposition='bottom right',line=dict(width=0.5))
        #fig.update_traces(line=dict(color="Black", width=0.5))

        self.fig_line.write_html(f'{graph_path}{pFilename}')
        self.graph_dict = {'graphname': f'{graph_path}{pFilename}', 'dimention': (pWidth, pHeight)}
        graphs_toshow_list.append(self.graph_dict)

    def mth_graph_choropleth(self,pDf_data,pLocations,pColor,pFilename,pWidth,pHeight,pTitle):
        self.fig_choropleth = px.choropleth(pDf_data,
                                            locations=pLocations,
                                            color=pColor,
                                            color_continuous_scale="Viridis_r",
                                            width  = pWidth - 50,
                                            height = pHeight - 50,
                                            )
        self.fig_choropleth.update_layout(
                                        title_text          =pTitle,
                                        title_font_family   ="Arial",
                                        title_font_size     =self.font_size1,
                                        title_font_color    ="black",
                                        title_x=0.45,
                                        )

        self.fig_choropleth.write_html(f'{graph_path}{pFilename}')
        self.graph_dict = {'graphname': f'{graph_path}{pFilename}', 'dimention': (pWidth, pHeight)}
        graphs_toshow_list.append(self.graph_dict)
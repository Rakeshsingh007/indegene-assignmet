from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework import status
import pandas as pd
import os
from assignment import settings

class GetAPI(APIView):

    """
    API to retrieve the data from CSV.

    """


    def get(self, request): 
        output_data = dict()
        output_data['caseNbr'] = "615524598"
        output_data['totalMarketValue'] = "$4,354,022"
        output_data['strategies']=list()
        output_data["productSegment"] = list()
        try:

            df_tab3_cur = pd.read_excel("/".join(('media','Technical_assessment_source_data.xlsx')), 'Table3,Current')
            strategy_data_tab3_cur = dict()
            strategy_data_tab3_cur["columns"] = list(df_tab3_cur.columns.values)
            for item in df_tab3_cur.iterrows():
                strategy_data_tab3_cur[item[1].array[0].replace(" ", "")] =[{"listRevenue":item[1].array[1],"expenditure":item[1].array[2],"discountPct":'{:,.2f}%'.format(item[1].array[3]*100)}]
            output_data['strategies'].append({"current":[strategy_data_tab3_cur]})


            df_tab3_tier = pd.read_excel("/".join(('media','Technical_assessment_source_data.xlsx')), 'Table3,Tier1')
            strategy_data_tab3_tier = dict()
            strategy_data_tab3_tier["columns"] = list(df_tab3_tier.columns.values)
            for index,item in enumerate(df_tab3_tier.iterrows()):
                strategy_data_tab3_tier[list(strategy_data_tab3_cur.keys())[1:][index]] =[{strategy_data_tab3_tier["columns"][0]:round(item[1].array[0]),strategy_data_tab3_tier["columns"][1]: '{:,.2f}%'.format(item[1].array[1]*100) ,strategy_data_tab3_tier["columns"][2]:'{:,.2f}%'.format(item[1].array[2]*100),strategy_data_tab3_tier["columns"][3]:round(item[1].array[3])}]
            output_data['strategies'][0]["tierOne"] = [strategy_data_tab3_tier]


            df_tab4_cur = pd.read_excel("/".join(('media','Technical_assessment_source_data.xlsx')), 'Table4,Current', )
            strategy_data_tab4_cur = dict()
            strategy_data_tab4_cur["columns"] = list(df_tab4_cur.columns.values)[1:]
            for index,item in enumerate(list(df_tab4_cur.iterrows())):
                strategy_data_tab4_cur[item[1]["Product Segment"]] =[{strategy_data_tab4_cur["columns"][0]:str(item[1]["totalMarketValue"]), strategy_data_tab4_cur["columns"][1]: str(item[1]["List Revenue"]), strategy_data_tab4_cur["columns"][2]:str(item[1]["Expenditure"]), strategy_data_tab4_cur["columns"][3]:'{:,.2f}%'.format(item[1]["Discount"]*100)}]
            output_data["productSegment"].append({"current":[strategy_data_tab4_cur]}) 


            df_tab4_tier = pd.read_excel("/".join(('media','Technical_assessment_source_data.xlsx')), 'Table4,Tier1')
            strategy_data_tab4_tier = dict()
            strategy_data_tab4_tier["columns"] = list(df_tab4_tier.columns.values)[1:]
            for index,item in enumerate(list(df_tab4_tier.iterrows())):
                strategy_data_tab4_tier[item[1]["Product Segment"]] =[{strategy_data_tab4_tier["columns"][0]:str(item[1]["Proposed"]), strategy_data_tab4_tier["columns"][1]: '{:,.2f}%'.format(item[1]["Disc %"]*100), strategy_data_tab4_tier["columns"][2]:str(item[1]["Industry Share (%)"]), strategy_data_tab4_tier["columns"][3]:str(item[1]["Impact"])}]
            output_data["productSegment"].append({"tierOne":[strategy_data_tab4_tier]}) 


            return Response({"status": "success", "data":  output_data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "failure", "data":  {'detail': 'Something went wrong'}}, status=status.HTTP_404_NOT_FOUND)
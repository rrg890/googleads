# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 20:26:28 2020

@author: ramon
"""

import datetime

from googleads import adwords


client = adwords.AdWordsClient.LoadFromStorage('googleads.yaml')


budget_service = client.GetService('BudgetService', version='v201809')
campaign_service = client.GetService('CampaignService', version='v201809')
ad_group_service = client.GetService('AdGroupService', version='v201809')
ad_group_criterion_service = client.GetService('AdGroupCriterionService', version='v201809')

budget = {
    'name': 'Budget HobbieCode',
    'amount': {
        'microAmount':30*1000000
    },
    'deliveryMethod': 'STANDARD'
}
budget_operations = [{
    'operator': 'ADD',
    'operand': budget
}]
        
# Add the budget.
budget_id = budget_service.mutate(budget_operations)['value'][0]['budgetId']
print('Budget creado')
# Construct operations and add campaigns.
operations = [{
  'operator': 'ADD',
  'operand': {
      'name': 'Campaña Search HobbieCode',
      # Recommendation: Set the campaign to PAUSED when creating it to
      # stop the ads from immediately serving. Set to ENABLED once you've
      # added targeting and the ads are ready to serve.
      'status': 'PAUSED',
      'advertisingChannelType': 'SEARCH',
      'biddingStrategyConfiguration': {
          'biddingStrategyType': 'MANUAL_CPC',
      },
      'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
      # Note that only the budgetId is required
      'budget': {
          'budgetId': budget_id
      },
      'networkSetting': {
          'targetGoogleSearch': 'true',
          'targetSearchNetwork': 'false',
          'targetContentNetwork': 'false',
          'targetPartnerSearchNetwork': 'false'
      },
      # Optional fields
      'startDate': (datetime.datetime.now() +
                        datetime.timedelta(1)).strftime('%Y%m%d'),
      'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          },
      'settings': [
          {
              'xsi_type': 'GeoTargetTypeSetting',
              'positiveGeoTargetType': 'DONT_CARE',
              'negativeGeoTargetType': 'DONT_CARE'
          }
      ]
  }
}, {
      'operator': 'ADD',
      'operand': {
          'name': 'Campaign Display HobbieCode',
          'status': 'PAUSED',
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPC'
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'advertisingChannelType': 'DISPLAY'
      }
}]

campaign_id = campaign_service.mutate(operations)['value'][0]['id']
print('Campaña creada')

operations = [{
  'operator': 'ADD',
  'operand': {
      'campaignId': campaign_id,
      'name': 'AD Group 1',
      'status': 'ENABLED',
      'biddingStrategyConfiguration': {
          'bids': [
              {
                  'xsi_type': 'CpcBid',
                  'bid': {
                      'microAmount': '1000000'
                  },
              }
          ]
      },
      'settings': [
          {
              # Targeting restriction settings. Depending on the
              # criterionTypeGroup value, most TargetingSettingDetail only
              # affect Display campaigns. However, the
              # USER_INTEREST_AND_LIST value works for RLSA campaigns -
              # Search campaigns targeting using a remarketing list.
              'xsi_type': 'TargetingSetting',
              'details': [
                  # Restricting to serve ads that match your ad group
                  # placements. This is equivalent to choosing
                  # "Target and bid" in the UI.
                  {
                      'xsi_type': 'TargetingSettingDetail',
                      'criterionTypeGroup': 'PLACEMENT',
                      'targetAll': 'false',
                  },
              ]
          }
      ]
  }
}]
ad_group_id = ad_group_service.mutate(operations)['value'][0]['id']
print('AD Group creado')
# Construct keyword ad group criterion object.
keyword1 = {
      'xsi_type': 'BiddableAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Keyword',
          'matchType': 'BROAD',
          'text': 'hobbicode'
      },
      # These fields are optional.
      'userStatus': 'PAUSED',
      'finalUrls': {
          'urls': ['https://www.hobbiecode.com/']
      }
}

keyword2 = {
      'xsi_type': 'BiddableAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Keyword',
          'matchType': 'BROAD',
          'text': 'machine learning'
      },
      # These fields are optional.
      'userStatus': 'PAUSED',
      'finalUrls': {
          'urls': ['https://www.hobbiecode.com/']
      }
}

stopword = {
      'xsi_type': 'NegativeAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Keyword',
          'matchType': 'EXACT',
          'text': 'coronavirus'
      }
}

  # Construct operations and add ad group criteria.
operations = [
      {
          'operator': 'ADD',
          'operand': keyword1
      },
      {
          'operator': 'ADD',
          'operand': keyword2
      },
      {
          'operator': 'ADD',
          'operand': stopword
      }
]
ad_group_criteria = ad_group_criterion_service.mutate(operations)['value']
print('Keywords creadas')
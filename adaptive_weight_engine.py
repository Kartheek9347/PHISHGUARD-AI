def prepare_feature_vector(features_dict):

    ordered_features = [
        features_dict["having_IP_Address"],
        features_dict["URL_Length"],
        features_dict["Shortining_Service"],
        features_dict["having_At_Symbol"],
        features_dict["double_slash_redirecting"],
        features_dict["Prefix_Suffix"],
        features_dict["having_Sub_Domain"],
        features_dict["SSLfinal_State"],
        features_dict["Domain_registeration_length"],
        features_dict["Favicon"],
        features_dict["port"],
        features_dict["HTTPS_token"],
        features_dict["Request_URL"],
        features_dict["URL_of_Anchor"],
        features_dict["Links_in_tags"],
        features_dict["SFH"],
        features_dict["Submitting_to_email"],
        features_dict["Abnormal_URL"],
        features_dict["Redirect"],
        features_dict["on_mouseover"],
        features_dict["RightClick"],
        features_dict["popUpWidnow"],
        features_dict["Iframe"],
        features_dict["age_of_domain"],
        features_dict["DNSRecord"],
        features_dict["web_traffic"],
        features_dict["Page_Rank"],
        features_dict["Google_Index"],
        features_dict["Links_pointing_to_page"],
        features_dict["Statistical_report"]
    ]

    return ordered_features
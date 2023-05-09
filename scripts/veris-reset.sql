SET foreign_key_checks = 0;


	truncate polls_veris_incident_details;
	truncate polls_veris_action_malware;
	
    truncate polls_veris_action_malware_notes;
	truncate polls_veris_action_malware_results;
	truncate polls_veris_action_malware_variety;
	truncate polls_veris_action_malware_vector;
	
    
    
    truncate polls_veris_action_hacking;
    truncate polls_veris_action_hacking_results;
    truncate polls_veris_action_hacking_variety;
    truncate polls_veris_action_hacking_vector;
    
    truncate polls_veris_action_social;
    truncate polls_veris_action_social_results;
    truncate polls_veris_action_social_target;
    truncate polls_veris_action_social_variety;
    truncate polls_veris_action_social_vector;  
    
    
    truncate polls_veris_action_misuse;
    truncate polls_veris_action_misuse_results;
    truncate polls_veris_action_misuse_target;
    truncate polls_veris_action_misuse_variety;
    truncate polls_veris_action_misuse_vector;   
    
    
    truncate polls_veris_action_physical;
    truncate polls_veris_action_physical_result;
    truncate polls_veris_action_physical_variety;
    truncate polls_veris_action_physical_vector;  
	truncate polls_veris_action_physical_location;
    
    
    truncate polls_veris_action_error;
    truncate polls_veris_action_error_variety;
    truncate polls_veris_action_error_vector;  
    
    truncate polls_veris_action_environmental;
    truncate polls_veris_action_environmental_variety;
    
    
    truncate polls_veris_actor;
    truncate polls_veris_actor_motive;
    truncate polls_veris_actor_origin;
    truncate polls_veris_actor_variety;  
    
    
    
    truncate polls_veris_asset;
    truncate polls_veris_asset_accessibility;
    truncate polls_veris_asset_cloud;
    truncate polls_veris_asset_hosting; 
	truncate polls_veris_asset_management;
	truncate polls_veris_asset_ownership;
    truncate polls_veris_asset_variety;
    
    truncate polls_veris_impact;
    truncate polls_veris_impact_loss;
    

SET foreign_key_checks = 1; 
/**
 * Field configuration for all claim forms
 * This single configuration file replaces 24 separate form components
 */

export interface FieldConfig {
  name: string
  label: string
  type: 'text' | 'textarea' | 'select' | 'date' | 'datetime' | 'radio' | 'checkbox' | 'tel' | 'number'
  required: boolean
  placeholder?: string
  maxLength?: number
  options?: Array<{ value: string; label: string }>
  dependsOn?: { field: string; value: string | string[] } // Show only if dependent field has this value
  characterCounter?: boolean
  helpText?: string
  validation?: 'fullName' | 'phone' | 'none'
  width?: '50%' | '100%' // Layout hint for side-by-side fields
}

export interface FieldGroupConfig {
  name: string
  fields: FieldConfig[]
}

// Common field groups used across multiple claim types
export const commonFieldGroups = {
  incidentDate: {
    name: 'incident_date',
    label: 'Incident Date *',
    type: 'date' as const,
    required: true,
    helpText: 'When did this incident occur?'
  },
  incidentSummary: {
    name: 'incident_summary',
    label: 'Brief Incident Summary *',
    type: 'textarea' as const,
    required: true,
    maxLength: 250,
    characterCounter: true,
    placeholder: 'Briefly describe what happened...'
  },
  additionalNotes: {
    name: 'additional_notes',
    label: 'Additional Notes',
    type: 'textarea' as const,
    required: false,
    maxLength: 250,
    characterCounter: true,
    placeholder: 'Any other information we should know...'
  },
  otherPartyInvolved: {
    name: 'other_party_involved',
    label: 'Other Party Involved? *',
    type: 'radio' as const,
    required: true,
    options: [
      { value: 'yes', label: 'Yes' },
      { value: 'no', label: 'No' }
    ]
  },
  otherPartyName: {
    name: 'other_party_name',
    label: 'Other Party Name *',
    type: 'text' as const,
    required: true,
    maxLength: 200,
    validation: 'fullName' as const,
    dependsOn: { field: 'other_party_involved', value: 'yes' },
    width: '50%' as const
  },
  otherPartyInsurance: {
    name: 'other_party_insurance',
    label: 'Insurance Company',
    type: 'text' as const,
    required: false,
    maxLength: 100,
    dependsOn: { field: 'other_party_involved', value: 'yes' },
    width: '50%' as const
  },
  policeReportFiled: {
    name: 'police_report_filed',
    label: 'Police Report Filed? *',
    type: 'radio' as const,
    required: true,
    options: [
      { value: 'yes', label: 'Yes' },
      { value: 'no', label: 'No' }
    ]
  },
  policeReportNumber: {
    name: 'police_report_number',
    label: 'Report Number *',
    type: 'text' as const,
    required: true,
    maxLength: 50,
    dependsOn: { field: 'police_report_filed', value: 'yes' }
  },
  policeDepartment: {
    name: 'police_department',
    label: 'Police Department *',
    type: 'text' as const,
    required: true,
    maxLength: 100,
    dependsOn: { field: 'police_report_filed', value: 'yes' }
  },
  damageDescription: {
    name: 'damage_description',
    label: 'Damage Description *',
    type: 'textarea' as const,
    required: true,
    maxLength: 250,
    characterCounter: true,
    placeholder: 'Describe the damage in detail...'
  }
}

/**
 * Claim field configurations by category and subcategory
 */
export const claimFieldsConfig: Record<string, FieldConfig[]> = {
  // Vehicle - Auto
  vehicle_auto: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'collision_vehicle', label: 'Collision with vehicle' },
        { value: 'collision_object', label: 'Collision with object' },
        { value: 'hit_and_run', label: 'Hit and run' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'theft', label: 'Theft' },
        { value: 'glass_damage', label: 'Glass damage' },
        { value: 'weather_damage', label: 'Weather damage' },
        { value: 'animal_collision', label: 'Animal collision' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    commonFieldGroups.otherPartyInvolved,
    commonFieldGroups.otherPartyName,
    commonFieldGroups.otherPartyInsurance,
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'vehicle_drivable',
      label: 'Vehicle Drivable? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - Motorcycle
  vehicle_motorcycle: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'collision_vehicle', label: 'Collision with vehicle' },
        { value: 'collision_object', label: 'Collision with object' },
        { value: 'dropped_bike', label: 'Dropped bike' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'weather_damage', label: 'Weather damage' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    {
      name: 'protective_gear',
      label: 'Protective Gear Worn',
      type: 'checkbox',
      required: false,
      options: [
        { value: 'helmet', label: 'Helmet' },
        { value: 'jacket', label: 'Jacket' },
        { value: 'gloves', label: 'Gloves' },
        { value: 'boots', label: 'Boots' },
        { value: 'pants', label: 'Pants' },
        { value: 'none', label: 'None' }
      ]
    },
    commonFieldGroups.otherPartyInvolved,
    commonFieldGroups.otherPartyName,
    commonFieldGroups.otherPartyInsurance,
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'motorcycle_drivable',
      label: 'Motorcycle Drivable? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - ATV/Off-road
  vehicle_atv: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'rollover', label: 'Rollover' },
        { value: 'collision', label: 'Collision' },
        { value: 'mechanical_failure', label: 'Mechanical failure' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    {
      name: 'terrain_type',
      label: 'Terrain Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Terrain Type' },
        { value: 'trail', label: 'Trail' },
        { value: 'desert', label: 'Desert' },
        { value: 'mountain', label: 'Mountain' },
        { value: 'private_property', label: 'Private property' },
        { value: 'other', label: 'Other' }
      ]
    },
    commonFieldGroups.otherPartyInvolved,
    commonFieldGroups.otherPartyName,
    commonFieldGroups.otherPartyInsurance,
    {
      name: 'injuries_sustained',
      label: 'Injuries Sustained? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'medical_attention',
      label: 'Medical Attention Received? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ],
      dependsOn: { field: 'injuries_sustained', value: 'yes' }
    },
    {
      name: 'vehicle_operational',
      label: 'Vehicle Operational? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - Roadside
  vehicle_roadside: [
    {
      name: 'service_type',
      label: 'Service Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Service Type' },
        { value: 'flat_tire', label: 'Flat tire' },
        { value: 'dead_battery', label: 'Dead battery' },
        { value: 'lockout', label: 'Lockout' },
        { value: 'out_of_fuel', label: 'Out of fuel' },
        { value: 'tow_needed', label: 'Tow needed' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'service_location',
      label: 'Service Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where service was needed'
    },
    {
      name: 'service_datetime',
      label: 'Service Date/Time *',
      type: 'datetime',
      required: true,
      helpText: 'When did you need service?'
    },
    {
      name: 'service_provider',
      label: 'Service Provider',
      type: 'text',
      required: false,
      maxLength: 100,
      placeholder: 'Name of tow/service company if known'
    },
    {
      name: 'service_description',
      label: 'Service Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe what service was performed...'
    }
  ],

  // Vehicle - Snowmobile
  vehicle_snowmobile: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'collision', label: 'Collision' },
        { value: 'rollover', label: 'Rollover' },
        { value: 'avalanche', label: 'Avalanche' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'mechanical_failure', label: 'Mechanical failure' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    {
      name: 'weather_conditions',
      label: 'Weather Conditions *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Weather Conditions' },
        { value: 'clear', label: 'Clear' },
        { value: 'snowing', label: 'Snowing' },
        { value: 'icy', label: 'Icy' },
        { value: 'blizzard', label: 'Blizzard' },
        { value: 'poor_visibility', label: 'Poor visibility' }
      ]
    },
    commonFieldGroups.otherPartyInvolved,
    commonFieldGroups.otherPartyName,
    commonFieldGroups.otherPartyInsurance,
    {
      name: 'injuries_sustained',
      label: 'Injuries Sustained? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'medical_attention',
      label: 'Medical Attention Received? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ],
      dependsOn: { field: 'injuries_sustained', value: 'yes' }
    },
    {
      name: 'snowmobile_operational',
      label: 'Snowmobile Operational? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - Boat
  vehicle_boat: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'collision_vessel', label: 'Collision with vessel' },
        { value: 'collision_object', label: 'Collision with object' },
        { value: 'sinking', label: 'Sinking' },
        { value: 'fire', label: 'Fire' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'weather_damage', label: 'Weather damage' },
        { value: 'grounding', label: 'Grounding' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Location Type' },
        { value: 'lake', label: 'Lake' },
        { value: 'river', label: 'River' },
        { value: 'ocean', label: 'Ocean' },
        { value: 'marina', label: 'Marina' },
        { value: 'storage_facility', label: 'Storage facility' },
        { value: 'trailer', label: 'Trailer' }
      ]
    },
    {
      name: 'water_conditions',
      label: 'Water Conditions *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Water Conditions' },
        { value: 'calm', label: 'Calm' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'rough', label: 'Rough' },
        { value: 'storm', label: 'Storm' }
      ]
    },
    {
      name: 'other_vessel_involved',
      label: 'Other Vessel Involved? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'other_vessel_operator',
      label: 'Other Vessel Operator Name *',
      type: 'text',
      required: true,
      maxLength: 200,
      validation: 'fullName',
      dependsOn: { field: 'other_vessel_involved', value: 'yes' }
    },
    {
      name: 'other_vessel_registration',
      label: 'Other Vessel Registration',
      type: 'text',
      required: false,
      maxLength: 50,
      dependsOn: { field: 'other_vessel_involved', value: 'yes' }
    },
    {
      name: 'coast_guard_report',
      label: 'Coast Guard Report Filed? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'coast_guard_report_number',
      label: 'Report Number *',
      type: 'text',
      required: true,
      maxLength: 50,
      dependsOn: { field: 'coast_guard_report', value: 'yes' }
    },
    {
      name: 'boat_operational',
      label: 'Boat Operational? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - RV
  vehicle_rv: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'collision', label: 'Collision' },
        { value: 'fire', label: 'Fire' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'weather_damage', label: 'Weather damage' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'appliance_failure', label: 'Appliance failure' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    {
      name: 'rv_in_motion',
      label: 'RV in Motion When Incident Occurred? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.otherPartyInvolved,
    commonFieldGroups.otherPartyName,
    commonFieldGroups.otherPartyInsurance,
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'rv_drivable',
      label: 'RV Drivable? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'living_quarters_affected',
      label: 'Living Quarters Affected? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Vehicle - Vehicle Protection
  vehicle_vehicle_protection: [
    {
      name: 'issue_type',
      label: 'Issue Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Issue Type' },
        { value: 'mechanical_breakdown', label: 'Mechanical breakdown' },
        { value: 'engine_failure', label: 'Engine failure' },
        { value: 'transmission_failure', label: 'Transmission failure' },
        { value: 'electrical_issue', label: 'Electrical issue' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'current_mileage',
      label: 'Current Mileage *',
      type: 'number',
      required: true,
      placeholder: 'e.g., 45000'
    },
    {
      name: 'warning_signs',
      label: 'Warning Signs Before Failure',
      type: 'textarea',
      required: false,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe any warning signs you noticed before failure...'
    },
    {
      name: 'vehicle_operable',
      label: 'Vehicle Currently Operable? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'issue_description',
      label: 'Issue Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the issue in detail...'
    }
  ],

  // Property - Homeowners
  property_homeowners: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'wind_damage', label: 'Wind damage' },
        { value: 'hail_damage', label: 'Hail damage' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'tree_damage', label: 'Tree damage' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'area_affected',
      label: 'Area Affected (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'roof', label: 'Roof' },
        { value: 'exterior_walls', label: 'Exterior walls' },
        { value: 'interior', label: 'Interior' },
        { value: 'kitchen', label: 'Kitchen' },
        { value: 'bathroom', label: 'Bathroom' },
        { value: 'bedrooms', label: 'Bedrooms' },
        { value: 'basement', label: 'Basement' },
        { value: 'garage', label: 'Garage' },
        { value: 'yard', label: 'Yard' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'damage_extent',
      label: 'Damage Extent *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Damage Extent' },
        { value: 'minor', label: 'Minor' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'severe', label: 'Severe' },
        { value: 'catastrophic', label: 'Catastrophic' }
      ]
    },
    {
      name: 'emergency_repairs_needed',
      label: 'Emergency Repairs Needed? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'currently_living_in_home',
      label: 'Currently Living in Home? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    commonFieldGroups.damageDescription
  ],

  // Property - Renters
  property_renters: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'theft', label: 'Theft' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'items_affected',
      label: 'Items Affected (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'electronics', label: 'Electronics' },
        { value: 'furniture', label: 'Furniture' },
        { value: 'clothing', label: 'Clothing' },
        { value: 'jewelry', label: 'Jewelry' },
        { value: 'appliances', label: 'Appliances' },
        { value: 'other_personal_property', label: 'Other personal property' }
      ]
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'landlord_notified',
      label: 'Landlord Notified? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Property - Condo
  property_condo: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'wind_damage', label: 'Wind damage' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'area_affected',
      label: 'Area Affected (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'unit_interior', label: 'Unit interior' },
        { value: 'balcony_patio', label: 'Balcony/Patio' },
        { value: 'personal_property', label: 'Personal property' },
        { value: 'common_area', label: 'Common area' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'damage_extent',
      label: 'Damage Extent *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Damage Extent' },
        { value: 'minor', label: 'Minor' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'severe', label: 'Severe' },
        { value: 'catastrophic', label: 'Catastrophic' }
      ]
    },
    {
      name: 'hoa_notified',
      label: 'HOA Notified? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'common_area_issue',
      label: 'Common Area Issue? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'currently_living_in_unit',
      label: 'Currently Living in Unit? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Property - Landlord
  property_landlord: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'wind_damage', label: 'Wind damage' },
        { value: 'tenant_damage', label: 'Tenant damage' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'tenant_involved',
      label: 'Tenant Involved? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'tenant_name',
      label: 'Tenant Name *',
      type: 'text',
      required: true,
      maxLength: 200,
      validation: 'fullName',
      dependsOn: { field: 'tenant_involved', value: 'yes' }
    },
    {
      name: 'tenant_caused_damage',
      label: 'Tenant Caused Damage? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ],
      dependsOn: { field: 'tenant_involved', value: 'yes' }
    },
    {
      name: 'property_occupied',
      label: 'Property Currently Occupied? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'rent_interruption',
      label: 'Rent Interruption Expected? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Property - Mobile Home
  property_mobile_home: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'wind_damage', label: 'Wind damage' },
        { value: 'structural_damage', label: 'Structural damage' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'area_affected',
      label: 'Area Affected (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'roof', label: 'Roof' },
        { value: 'exterior', label: 'Exterior' },
        { value: 'interior', label: 'Interior' },
        { value: 'skirting', label: 'Skirting' },
        { value: 'deck_steps', label: 'Deck/Steps' },
        { value: 'shed', label: 'Shed' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'damage_extent',
      label: 'Damage Extent *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Damage Extent' },
        { value: 'minor', label: 'Minor' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'severe', label: 'Severe' },
        { value: 'catastrophic', label: 'Catastrophic' }
      ]
    },
    {
      name: 'mobile_home_movable',
      label: 'Mobile Home Movable? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'currently_living_in_mobile_home',
      label: 'Currently Living in Mobile Home? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    commonFieldGroups.damageDescription
  ],

  // Life
  life: [
    {
      name: 'claim_type',
      label: 'Claim Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Claim Type' },
        { value: 'death', label: 'Death of insured' },
        { value: 'terminal_illness', label: 'Terminal illness diagnosis' },
        { value: 'critical_illness', label: 'Critical illness diagnosis' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'date_of_event',
      label: 'Date of Death/Diagnosis *',
      type: 'date',
      required: true,
      helpText: 'Date of death or diagnosis'
    },
    {
      name: 'physician_name',
      label: 'Physician Name',
      type: 'text',
      required: false,
      maxLength: 100
    },
    {
      name: 'medical_facility',
      label: 'Medical Facility',
      type: 'text',
      required: false,
      maxLength: 100
    },
    {
      name: 'brief_description',
      label: 'Brief Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Please provide a brief description...'
    }
  ],

  // Business
  business: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'property_damage', label: 'Property damage' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'business_interruption', label: 'Business interruption' },
        { value: 'employee_injury', label: 'Employee injury' },
        { value: 'data_breach', label: 'Data breach' },
        { value: 'theft', label: 'Theft' },
        { value: 'vandalism', label: 'Vandalism' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'business_status',
      label: 'Business Operational Status *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Status' },
        { value: 'fully_operational', label: 'Fully operational' },
        { value: 'partially_operational', label: 'Partially operational' },
        { value: 'temporarily_closed', label: 'Temporarily closed' }
      ]
    },
    {
      name: 'employees_affected',
      label: 'Employees Affected? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'third_parties_involved',
      label: 'Third Parties Involved? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'third_party_type',
      label: 'Third Party Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Type' },
        { value: 'customer', label: 'Customer' },
        { value: 'vendor', label: 'Vendor' },
        { value: 'contractor', label: 'Contractor' },
        { value: 'other_business', label: 'Other business' },
        { value: 'other', label: 'Other' }
      ],
      dependsOn: { field: 'third_parties_involved', value: 'yes' }
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the incident in detail...'
    }
  ],

  // Identity Protection
  identity_protection: [
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'credit_card_fraud', label: 'Credit card fraud' },
        { value: 'bank_account_fraud', label: 'Bank account fraud' },
        { value: 'identity_theft', label: 'Identity theft' },
        { value: 'data_breach', label: 'Data breach' },
        { value: 'phishing', label: 'Phishing' },
        { value: 'tax_fraud', label: 'Tax fraud' },
        { value: 'medical_identity_theft', label: 'Medical identity theft' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'date_discovered',
      label: 'Date Discovered *',
      type: 'date',
      required: true,
      helpText: 'When did you discover the incident?'
    },
    {
      name: 'accounts_affected',
      label: 'Accounts Affected (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'bank_account', label: 'Bank account' },
        { value: 'credit_card', label: 'Credit card' },
        { value: 'investment_account', label: 'Investment account' },
        { value: 'social_security', label: 'Social Security' },
        { value: 'medical_records', label: 'Medical records' },
        { value: 'tax_records', label: 'Tax records' },
        { value: 'other', label: 'Other' }
      ]
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'financial_institutions_notified',
      label: 'Financial Institutions Notified? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'credit_bureaus_notified',
      label: 'Credit Bureaus Notified? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the incident in detail...'
    }
  ],

  // Other - Personal Umbrella Policy
  other_umbrella: [
    {
      name: 'underlying_incident_type',
      label: 'Underlying Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'auto_liability', label: 'Auto liability' },
        { value: 'home_liability', label: 'Home liability' },
        { value: 'boat_liability', label: 'Boat liability' },
        { value: 'business_liability', label: 'Business liability' },
        { value: 'other_liability', label: 'Other liability' }
      ]
    },
    {
      name: 'primary_insurance_claim_filed',
      label: 'Primary Insurance Claim Filed? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'primary_insurance_company',
      label: 'Primary Insurance Company *',
      type: 'text',
      required: true,
      maxLength: 100,
      dependsOn: { field: 'primary_insurance_claim_filed', value: 'yes' }
    },
    {
      name: 'third_party_involved',
      label: 'Third Party Involved? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'lawsuit_filed',
      label: 'Lawsuit Filed? *',
      type: 'radio',
      required: true,
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the incident in detail...'
    }
  ],

  // Other - Individual Health
  other_individual_health: [
    {
      name: 'service_type',
      label: 'Service Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Service Type' },
        { value: 'medical_procedure', label: 'Medical procedure' },
        { value: 'hospital_stay', label: 'Hospital stay' },
        { value: 'emergency_care', label: 'Emergency care' },
        { value: 'prescription', label: 'Prescription' },
        { value: 'medical_equipment', label: 'Medical equipment' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'service_date',
      label: 'Service Date *',
      type: 'date',
      required: true,
      helpText: 'When did you receive this service?'
    },
    {
      name: 'healthcare_provider',
      label: 'Healthcare Provider *',
      type: 'text',
      required: true,
      maxLength: 100,
      placeholder: 'Name of hospital, clinic, or provider'
    },
    {
      name: 'provider_type',
      label: 'Provider Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Provider Type' },
        { value: 'hospital', label: 'Hospital' },
        { value: 'clinic', label: 'Clinic' },
        { value: 'doctors_office', label: "Doctor's office" },
        { value: 'urgent_care', label: 'Urgent care' },
        { value: 'emergency_room', label: 'Emergency room' },
        { value: 'pharmacy', label: 'Pharmacy' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'service_description',
      label: 'Service Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the service received...'
    }
  ],

  // Other - Pet
  other_pet: [
    {
      name: 'pet_name',
      label: 'Pet Name *',
      type: 'text',
      required: true,
      maxLength: 50
    },
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'illness', label: 'Illness' },
        { value: 'injury', label: 'Injury' },
        { value: 'surgery', label: 'Surgery' },
        { value: 'emergency_care', label: 'Emergency care' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'treatment_date',
      label: 'Treatment Date *',
      type: 'date',
      required: true,
      helpText: 'When was your pet treated?'
    },
    {
      name: 'veterinary_clinic',
      label: 'Veterinary Clinic *',
      type: 'text',
      required: true,
      maxLength: 100,
      placeholder: 'Name of clinic or hospital'
    },
    {
      name: 'treatment_description',
      label: 'Treatment Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the treatment received...'
    }
  ],

  // Other - Event
  other_event: [
    {
      name: 'event_name',
      label: 'Event Name *',
      type: 'text',
      required: true,
      maxLength: 100,
      placeholder: 'Name of the event'
    },
    {
      name: 'event_date',
      label: 'Event Date *',
      type: 'date',
      required: true,
      helpText: 'Scheduled event date'
    },
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'cancellation', label: 'Cancellation' },
        { value: 'postponement', label: 'Postponement' },
        { value: 'property_damage', label: 'Property damage' },
        { value: 'liability_claim', label: 'Liability claim' },
        { value: 'vendor_no_show', label: 'Vendor no-show' },
        { value: 'weather', label: 'Weather' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'cancellation_date',
      label: 'Cancellation/Incident Date *',
      type: 'date',
      required: true,
      helpText: 'When was the event cancelled or incident occurred?'
    },
    {
      name: 'reason_description',
      label: 'Reason Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe why the event was cancelled or what happened...'
    }
  ],

  // Other - Travel
  other_travel: [
    {
      name: 'trip_destination',
      label: 'Trip Destination *',
      type: 'text',
      required: true,
      maxLength: 100,
      placeholder: 'Where were you traveling to?'
    },
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'trip_cancellation', label: 'Trip cancellation' },
        { value: 'trip_interruption', label: 'Trip interruption' },
        { value: 'baggage_loss', label: 'Baggage loss' },
        { value: 'baggage_delay', label: 'Baggage delay' },
        { value: 'medical_emergency', label: 'Medical emergency' },
        { value: 'travel_delay', label: 'Travel delay' },
        { value: 'missed_connection', label: 'Missed connection' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'scheduled_departure',
      label: 'Scheduled Departure Date *',
      type: 'date',
      required: true,
      helpText: 'When were you scheduled to depart?'
    },
    {
      name: 'incident_date',
      label: 'Incident Date *',
      type: 'date',
      required: true,
      helpText: 'When did the incident occur?'
    },
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe what happened...'
    }
  ],

  // Other - Jewelry
  other_jewelry: [
    {
      name: 'number_of_items',
      label: 'Number of Items Affected *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Number' },
        { value: '1', label: '1' },
        { value: '2', label: '2' },
        { value: '3', label: '3' },
        { value: '4', label: '4' },
        { value: '5+', label: '5+' }
      ]
    },
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'theft', label: 'Theft' },
        { value: 'loss', label: 'Loss' },
        { value: 'damage', label: 'Damage' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the incident in detail...'
    }
  ],

  // Other - Collectibles
  other_collectibles: [
    {
      name: 'number_of_items',
      label: 'Number of Items Affected *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Number' },
        { value: '1', label: '1' },
        { value: '2-5', label: '2-5' },
        { value: '6-10', label: '6-10' },
        { value: '11+', label: '11+' }
      ]
    },
    {
      name: 'item_types',
      label: 'Item Types (select all that apply) *',
      type: 'checkbox',
      required: true,
      options: [
        { value: 'art', label: 'Art' },
        { value: 'coins', label: 'Coins' },
        { value: 'stamps', label: 'Stamps' },
        { value: 'sports_memorabilia', label: 'Sports memorabilia' },
        { value: 'antiques', label: 'Antiques' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_type',
      label: 'Incident Type *',
      type: 'select',
      required: true,
      options: [
        { value: '', label: 'Select Incident Type' },
        { value: 'theft', label: 'Theft' },
        { value: 'fire', label: 'Fire' },
        { value: 'water_damage', label: 'Water damage' },
        { value: 'damage', label: 'Damage' },
        { value: 'other', label: 'Other' }
      ]
    },
    {
      name: 'incident_location',
      label: 'Incident Location *',
      type: 'text',
      required: true,
      maxLength: 250,
      placeholder: 'General location where incident occurred'
    },
    commonFieldGroups.policeReportFiled,
    commonFieldGroups.policeReportNumber,
    commonFieldGroups.policeDepartment,
    {
      name: 'incident_description',
      label: 'Incident Description *',
      type: 'textarea',
      required: true,
      maxLength: 250,
      characterCounter: true,
      placeholder: 'Describe the incident in detail...'
    }
  ]
}

/**
 * Get field configuration for a specific claim type
 */
export function getClaimFields(category: string, subcategory: string | null): FieldConfig[] {
  const key = subcategory ? `${category}_${subcategory}` : category
  return claimFieldsConfig[key] || []
}

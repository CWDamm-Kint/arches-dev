define([
    'arches',
    'knockout',
    'templates/views/components/map-popup.htm'
], function(arches, ko, popupTemplate) {

    var provider = {

        /**
         * Callback to determine if the feature is clickable
         * @param feature Map feature to check
         * @returns <code>true</code> if the feature can be clicked, otherwise <code>false</code>
         */
        isFeatureClickable: function(feature, map)
        {
            const selectedFeatureIds = ko.unwrap(map.selectedFeatureIds);
            const selectedTool = ko.unwrap(map.selectedTool);
            if ((typeof selectedTool !== 'undefined' && selectedTool !== null) || selectedFeatureIds && selectedFeatureIds.length)
                return false;
            return feature.properties.resourceinstanceid;
        },

        /**
         * Return the template that should be used for the
         * @param features - Unused in this provider, but may be used in custom provider to determine which template
         * to use
         * @returns {*} HTML template for the Map Popup
         */
        getPopupTemplate: function(features)
        {
            return popupTemplate;
        },

        /**
         * Each feature in the list must have a <code>displayname</code> and <code>map_popup</code> value. This is
         * handled for arches resources by the framework, but can be injected here if any of the features.popupFeatures
         * do not have one.
         */
        processData: function(features)
        {
            return features;
        },

        /**
         * This method enables custom logic for how the feature in the popup should be handled and/or mutated en route to the mapFilter.
         * @param popupFeatureObject - the javascript object of the feature and its associated contexts (e.g. mapCard).
         * @param featureGeomIndex - int index corresponding to the feature that was clicked, used for lookup against an arry of geoms
         * @required @method mapCard.filterByFeatureGeom()
         * @required @send argument: @param feature - a geojson feature object 
         * with an @optional @property: feature.id corresponding to a uuid for that tile_geometrycollection_feature
         * @optional @send argument: @param resourceid
         */
        sendFeatureToMapFilter: function(popupFeatureObject, featureGeomIndex)
        {
            let feature = popupFeatureObject.geometries()[featureGeomIndex].geom.features[0];
            popupFeatureObject.mapCard.filterByFeatureGeom(feature, popupFeatureObject.resourceinstanceid);
        },

        /**
         * Determines whether to show the button for Filter By Feature
         * @param popupFeatureObject - the javascript object of the feature and its associated contexts (e.g. mapCard).
         * @param featureGeomIndex - int index corresponding to the feature that was clicked, used for lookup against an arry of geoms
         * @returns {boolean} - whether to show "Filter by Feature" on map popup
         * typically dependent on at least 1 feature with a geometry and/or a featureid/resourceid combo
         */
        showFilterByFeature: function(popupFeatureObject, featureGeomIndex) {
            return (ko.unwrap(popupFeatureObject.geometries) || []).length > 0;
        },

    };
    return provider;
});

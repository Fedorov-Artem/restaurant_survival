window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, context) {
            const {
                circleOptions,
                color
            } = context.hideout;
            circleOptions.fillColor = feature.properties.color; // set color based on color prop
            return L.circleMarker(latlng, circleOptions); // render a simple circle marker
        }
    }
});
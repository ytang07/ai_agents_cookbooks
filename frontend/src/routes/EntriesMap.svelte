<script>
    // Set up google maps
    let map;
    let markers = [];
    let infoWindow;
    let bounds;
    let mapOptions = {
        center: { lat: 0, lng: 0 },
        zoom: 2,
        mapTypeId: 'roadmap',
    };

</script>

<!-- Set up map -->

<div id="map" bind:this={map} style="height: 100vh; width: 100%;">
</div>

const user = JSON.parse(document.getElementById('user_json').textContent);
const task = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app1',
    data: {
        users: [],
    },
    mounted() {
        const host = `${window.location.protocol}//${window.location.host}`;
        axios
            .get(host + '/api/useraccount/')
            .then(response => (this.users = response.data)); 
    }
});
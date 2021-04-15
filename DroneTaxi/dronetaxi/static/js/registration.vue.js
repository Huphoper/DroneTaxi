const task = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        useraccount: {
            date_of_birth: null,
            gender: null,
            photo: null,
        },
        createSuccess: false,
    },
    methods: {
        async createUser() {
            const host = `${window.location.protocol}//${window.location.host}`;
            await axios.post(host + '/api/useraccount/', this.useraccount, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((response) => {
                console.log(response);
                this.createSuccess = true;
            })
            .catch((error) => {
                console.log(error);
            });
        }
    },
});
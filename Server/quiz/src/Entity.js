class Entity {
    static async sendCorrectIncorrect(known, unknown) {
        return fetch(`http://ai4good-translation.herokuapp.com/quiz-results?ip=192.108.108.45&known=${ known }&unknown=${ unknown }`)
        .then(result => result.json()).then(json => { console.log(json); });
    }
}

exports.Entity = Entity;
export class Serializable {

    fromJSON(json: Object) {
        for (var propName in json)
            this[propName] = json[propName];
        return this;
    }
}

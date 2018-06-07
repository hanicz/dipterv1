import { Serializable } from '../utils/serializable'

export class TravelPlan{
    public id: Number;
    public lng: Number;
    public lat: Number;
    public label: String;
    public static draggable: false;
}
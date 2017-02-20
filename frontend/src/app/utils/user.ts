/**
 * Created by Hanicz on 2/19/2017.
 */
import { Serializable } from '../utils/serializable'

export class User extends Serializable{
  id:number;
  name:string;
  email: string;
}

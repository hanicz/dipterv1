/**
 * Created by Hanicz on 2/19/2017.
 */
import { Serializable } from '../utils/serializable'

export class User extends Serializable{
    constructor(
    public username: string,
    public email: string,
    public password: string
  ) { super() }

}

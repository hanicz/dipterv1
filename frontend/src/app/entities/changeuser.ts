/**
 * Created by Hanicz on 2/19/2017.
 */
import { Serializable } from '../utils/serializable'

export class ChangeUser extends Serializable{
    public old_password: string;
    public new_password: string;
    public new_email: string;

}

import 'package:coex_clover/model/aule.dart';
import 'package:http/http.dart' as http;

class DroneApi {
  String _urlServer;

  DroneApi(String urlServer) {
    _urlServer = urlServer;
  }

  Future<bool> goTo(Aule aula) async {
    var response = await http.get(
      Uri.parse(/*"$_urlServer/" + aula.toShortString()*/'http://127.0.0.1:5000/prova'),
    );
    return response.statusCode == 200;
  }
}

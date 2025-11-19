class UserModel {
  final int id;
  final String email;
  final String name;
  final String? state;
  final String? district;
  final List<String> preferredLanguages;
  final List<String> interests;
  final String role;
  final DateTime dateJoined;

  UserModel({
    required this.id,
    required this.email,
    required this.name,
    this.state,
    this.district,
    required this.preferredLanguages,
    required this.interests,
    required this.role,
    required this.dateJoined,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      state: json['state'],
      district: json['district'],
      preferredLanguages: List<String>.from(json['preferred_languages'] ?? []),
      interests: List<String>.from(json['interests'] ?? []),
      role: json['role'] ?? 'citizen',
      dateJoined: DateTime.parse(json['date_joined']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'state': state,
      'district': district,
      'preferred_languages': preferredLanguages,
      'interests': interests,
      'role': role,
      'date_joined': dateJoined.toIso8601String(),
    };
  }
}

class AuthResponse {
  final UserModel user;
  final String accessToken;
  final String refreshToken;

  AuthResponse({
    required this.user,
    required this.accessToken,
    required this.refreshToken,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      user: UserModel.fromJson(json['user']),
      accessToken: json['tokens']['access'],
      refreshToken: json['tokens']['refresh'],
    );
  }
}

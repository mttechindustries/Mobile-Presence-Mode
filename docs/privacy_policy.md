# Privacy Policy for Mobile Presence Mode

## Overview

Mobile Presence Mode is designed with privacy as a core principle. Unlike many sensing technologies that rely on cloud processing or external sensors, our framework operates entirely on-device using signals that you control.

## Data Collection and Processing

### What We Collect

Mobile Presence Mode only collects and processes:

1. **Wi-Fi Channel State Information (CSI)**: Technical data about Wi-Fi signal propagation
2. **Timestamps**: When measurements were taken
3. **Device Information**: Basic device identifiers for CSI processing

### What We Don't Collect

We explicitly do **NOT** collect:

- Personal identifiable information (PII)
- Location data (GPS, Wi-Fi positioning)
- Audio or video recordings
- Device contacts, messages, or files
- Network traffic content
- Any data not essential for presence detection

## Data Storage

### Local Storage Only

- All CSI data is stored locally on your device
- No data is transmitted to cloud servers by default
- You have full control over data retention and deletion

### Optional Cloud Features

If you choose to enable optional cloud features (disabled by default):

- Data is encrypted in transit (TLS 1.3+)
- Data is anonymized before transmission
- You can opt-out at any time
- All cloud processing is clearly disclosed

## Data Usage

### Primary Uses

Collected CSI data is used solely for:

1. **Presence Detection**: Determining if humans/pets are present
2. **Breathing Analysis**: Estimating breathing rates
3. **Performance Improvement**: Local algorithm optimization

### Prohibited Uses

We will never use your data for:

- Advertising or marketing
- Third-party data sharing
- Behavioral profiling
- Location tracking
- Any purpose not explicitly related to presence detection

## Data Sharing

### No Third-Party Sharing

- Your CSI data is never shared with third parties
- We don't sell or rent your data
- No data brokers or analytics companies have access

### Open Source Transparency

- All data processing code is open source
- You can audit exactly what happens to your data
- No hidden data collection mechanisms

## Security Measures

### Data Protection

- CSI data is encrypted at rest when stored
- All communications use strong encryption
- Regular security audits of our codebase

### Access Control

- Only you can access your CSI data
- No remote access capabilities built-in
- All processing happens on your device

## User Rights

### Your Data, Your Control

You have the right to:

1. **Access**: View all data collected by the system
2. **Delete**: Remove any or all collected data
3. **Export**: Get your data in standard formats
4. **Opt-Out**: Disable any data collection features
5. **Audit**: Review the source code for compliance

### Data Retention

- CSI data is kept only as long as needed
- Default retention: 24 hours for processing
- You can configure shorter retention periods
- Automatic deletion when app is uninstalled

## Compliance

### Legal Standards

While not legally required for this type of technical data, we voluntarily comply with:

- **GDPR principles**: Data minimization, purpose limitation
- **CCPA spirit**: Transparency, user control
- **Ethical AI guidelines**: Privacy-by-design approach

### Research Use

If you contribute data to our open research dataset:

- All data is fully anonymized
- Explicit opt-in required
- Clear explanation of research purposes
- Right to withdraw consent anytime

## Technical Safeguards

### On-Device Processing

- All CSI analysis happens on your device
- No raw CSI data leaves your device by default
- Processing results stay local unless you choose to share

### Minimal Data Collection

- We collect only what's necessary for functionality
- No unnecessary metadata collection
- Regular reviews to minimize data footprint

### Transparent Algorithms

- All detection algorithms are open source
- No proprietary "black box" processing
- You can verify what happens to your data

## Comparison with Other Technologies

### Mobile Presence Mode vs Traditional Sensors

| Aspect | Mobile Presence Mode | Radar Sensors | Camera Systems | Microphones |
|--------|----------------------|---------------|----------------|-------------|
| **Data Type** | Wi-Fi signals | Radio waves | Visual images | Audio recordings |
| **Privacy Risk** | Low | Medium | High | High |
| **Identifiability** | None | None | High | High |
| **Cloud Dependency** | Optional | Often required | Often required | Often required |
| **User Control** | Full | Limited | Limited | Limited |

## Ethical Considerations

### Responsible Use

We encourage users to:

- Use only in spaces where you have consent
- Be transparent about monitoring capabilities
- Respect others' privacy expectations
- Comply with local laws and regulations

### Prohibited Applications

Mobile Presence Mode should not be used for:

- Surveillance without consent
- Employee monitoring without disclosure
- Any illegal or unethical purposes
- Medical diagnosis without proper validation

## Future Commitments

As we develop this framework, we commit to:

1. **Privacy-by-Design**: Privacy considerations in every feature
2. **Transparency**: Clear documentation of all data flows
3. **User Empowerment**: Tools for users to control their data
4. **Regular Audits**: Independent reviews of our privacy practices
5. **Community Oversight**: Open governance of privacy policies

## Contact

For privacy-related questions or concerns:

- Open a GitHub issue with "Privacy" label
- All issues are public and transparent
- Community-driven resolution process

## Changes to This Policy

- Any changes will be documented in GitHub commits
- Major changes will be announced in release notes
- You can always review the full history of this document

**Last Updated**: 2024
**Effective Date**: Immediate upon installation

This privacy policy reflects our commitment to responsible, ethical development of sensing technologies that respect user privacy while providing innovative functionality.
